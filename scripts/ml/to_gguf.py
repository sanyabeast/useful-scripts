import sys
import os
import json
import struct
import time
import argparse
from enum import IntEnum, auto
from typing import Dict, List, Tuple, Optional, Any, Union
from tqdm import tqdm

import numpy as np
import torch
from safetensors.torch import load_file

# GGUF format constants based on llama.cpp implementation
class GGUFValueType(IntEnum):
    UINT8   = 0
    INT8    = 1
    UINT16  = 2
    INT16   = 3
    UINT32  = 4
    INT32   = 5
    FLOAT32 = 6
    BOOL    = 7
    STRING  = 8
    ARRAY   = 9
    UINT64  = 10
    INT64   = 11
    FLOAT64 = 12

class GGUFTensorType(IntEnum):
    F32 = 0
    F16 = 1
    Q4_0 = 2
    Q4_1 = 3
    Q5_0 = 4
    Q5_1 = 5
    Q8_0 = 6
    Q8_1 = 7
    Q2_K = 8
    Q3_K = 9
    Q4_K = 10
    Q5_K = 11
    Q6_K = 12
    Q8_K = 13
    I8 = 14
    I16 = 15
    I32 = 16
    COUNT = 17

class Logger:
    """Fancy emoji logger for the conversion process"""
    
    EMOJIS = {
        "start": "🚀",
        "load": "📂",
        "validate": "✅",
        "convert": "🔄",
        "quantize": "⚙️",
        "save": "💾",
        "tensor": "🧩",
        "metadata": "📋",
        "success": "✨",
        "error": "❌",
        "warning": "⚠️",
        "info": "ℹ️",
        "memory": "🧠",
        "time": "⏱️"
    }
    
    @staticmethod
    def log(type_: str, message: str):
        emoji = Logger.EMOJIS.get(type_, "🔍")
        print(f"{emoji} {message}")
    
    @staticmethod
    def progress(iterable, desc: str, **kwargs):
        emoji = Logger.EMOJIS.get(desc.lower().split()[0], "🔄")
        return tqdm(iterable, desc=f"{emoji} {desc}", **kwargs)

def get_tensor_type(tensor: torch.Tensor, quantization: Optional[str] = None) -> GGUFTensorType:
    """Map tensor dtype to GGUF tensor type"""
    if quantization:
        if quantization == "q4_0":
            return GGUFTensorType.Q4_0
        elif quantization == "q4_1":
            return GGUFTensorType.Q4_1
        elif quantization == "q5_0":
            return GGUFTensorType.Q5_0
        elif quantization == "q5_1":
            return GGUFTensorType.Q5_1
        elif quantization == "q8_0":
            return GGUFTensorType.Q8_0
        elif quantization == "q2_k":
            return GGUFTensorType.Q2_K
        elif quantization == "q3_k":
            return GGUFTensorType.Q3_K
        elif quantization == "q4_k":
            return GGUFTensorType.Q4_K
        elif quantization == "q5_k":
            return GGUFTensorType.Q5_K
        elif quantization == "q6_k":
            return GGUFTensorType.Q6_K
        elif quantization == "q8_k":
            return GGUFTensorType.Q8_K
        else:
            raise ValueError(f"Unsupported quantization type: {quantization}")
    
    if tensor.dtype == torch.float32:
        return GGUFTensorType.F32
    elif tensor.dtype == torch.float16:
        return GGUFTensorType.F16
    elif tensor.dtype == torch.int8:
        return GGUFTensorType.I8
    elif tensor.dtype == torch.int16:
        return GGUFTensorType.I16
    elif tensor.dtype == torch.int32:
        return GGUFTensorType.I32
    else:
        # Convert unsupported types to F32
        return GGUFTensorType.F32

def write_gguf_header(f):
    """Write the GGUF magic and version"""
    f.write(b"GGUF")  # Magic
    f.write(struct.pack("<I", 2))  # Version 2

def write_gguf_value(f, type_: GGUFValueType, value: Any):
    """Write a value to the GGUF file with its type"""
    f.write(struct.pack("<I", int(type_)))
    
    if type_ == GGUFValueType.UINT8:
        f.write(struct.pack("<B", value))
    elif type_ == GGUFValueType.INT8:
        f.write(struct.pack("<b", value))
    elif type_ == GGUFValueType.UINT16:
        f.write(struct.pack("<H", value))
    elif type_ == GGUFValueType.INT16:
        f.write(struct.pack("<h", value))
    elif type_ == GGUFValueType.UINT32:
        f.write(struct.pack("<I", value))
    elif type_ == GGUFValueType.INT32:
        f.write(struct.pack("<i", value))
    elif type_ == GGUFValueType.FLOAT32:
        f.write(struct.pack("<f", value))
    elif type_ == GGUFValueType.BOOL:
        f.write(struct.pack("<?", value))
    elif type_ == GGUFValueType.STRING:
        encoded = value.encode('utf-8')
        f.write(struct.pack("<Q", len(encoded)))
        f.write(encoded)
    elif type_ == GGUFValueType.UINT64:
        f.write(struct.pack("<Q", value))
    elif type_ == GGUFValueType.INT64:
        f.write(struct.pack("<q", value))
    elif type_ == GGUFValueType.FLOAT64:
        f.write(struct.pack("<d", value))
    elif type_ == GGUFValueType.ARRAY:
        # Array handling would be more complex
        raise NotImplementedError("Array type not implemented yet")
    else:
        raise ValueError(f"Unsupported value type: {type_}")

def write_gguf_metadata(f, metadata: Dict[str, Any]):
    """Write metadata to the GGUF file"""
    # Write number of metadata key-value pairs
    f.write(struct.pack("<Q", len(metadata)))
    
    # Write each key-value pair
    for key, value in metadata.items():
        # Write key
        encoded_key = key.encode('utf-8')
        f.write(struct.pack("<Q", len(encoded_key)))
        f.write(encoded_key)
        
        # Determine type and write value
        if isinstance(value, bool):
            write_gguf_value(f, GGUFValueType.BOOL, value)
        elif isinstance(value, int):
            if value >= 0:
                if value <= 255:
                    write_gguf_value(f, GGUFValueType.UINT8, value)
                elif value <= 65535:
                    write_gguf_value(f, GGUFValueType.UINT16, value)
                elif value <= 4294967295:
                    write_gguf_value(f, GGUFValueType.UINT32, value)
                else:
                    write_gguf_value(f, GGUFValueType.UINT64, value)
            else:
                if value >= -128 and value <= 127:
                    write_gguf_value(f, GGUFValueType.INT8, value)
                elif value >= -32768 and value <= 32767:
                    write_gguf_value(f, GGUFValueType.INT16, value)
                elif value >= -2147483648 and value <= 2147483647:
                    write_gguf_value(f, GGUFValueType.INT32, value)
                else:
                    write_gguf_value(f, GGUFValueType.INT64, value)
        elif isinstance(value, float):
            write_gguf_value(f, GGUFValueType.FLOAT32, value)
        elif isinstance(value, str):
            write_gguf_value(f, GGUFValueType.STRING, value)
        else:
            # Skip unsupported types
            Logger.log("warning", f"Skipping unsupported metadata type for key '{key}'")

def quantize_tensor(tensor: np.ndarray, quant_type: str) -> Tuple[np.ndarray, float, float]:
    """
    Quantize a tensor to the specified type.
    Returns the quantized tensor, scale, and zero point.
    """
    if quant_type.startswith("q4"):
        # 4-bit quantization
        abs_max = np.max(np.abs(tensor))
        scale = abs_max / 7.0  # Scale to fit in 4 bits (-7 to 7 range)
        
        # Quantize
        tensor_q = np.clip(np.round(tensor / scale), -7, 7).astype(np.int8)
        
        # For q4_1, we would compute per-block scales, but simplified here
        return tensor_q, scale, 0
        
    elif quant_type.startswith("q5"):
        # 5-bit quantization
        abs_max = np.max(np.abs(tensor))
        scale = abs_max / 15.0  # Scale to fit in 5 bits (-15 to 15 range)
        
        # Quantize
        tensor_q = np.clip(np.round(tensor / scale), -15, 15).astype(np.int8)
        return tensor_q, scale, 0
        
    elif quant_type.startswith("q8"):
        # 8-bit quantization
        abs_max = np.max(np.abs(tensor))
        scale = abs_max / 127.0  # Scale to fit in 8 bits (-127 to 127 range)
        
        # Quantize
        tensor_q = np.clip(np.round(tensor / scale), -127, 127).astype(np.int8)
        return tensor_q, scale, 0
        
    elif quant_type.startswith("q2_k"):
        # 2-bit k-quantization (simplified)
        abs_max = np.max(np.abs(tensor))
        scale = abs_max / 1.0  # Scale to fit in 2 bits (-1 to 1 range)
        
        # Quantize
        tensor_q = np.clip(np.round(tensor / scale), -1, 1).astype(np.int8)
        return tensor_q, scale, 0
        
    elif quant_type.startswith("q3_k"):
        # 3-bit k-quantization (simplified)
        abs_max = np.max(np.abs(tensor))
        scale = abs_max / 3.0  # Scale to fit in 3 bits (-3 to 3 range)
        
        # Quantize
        tensor_q = np.clip(np.round(tensor / scale), -3, 3).astype(np.int8)
        return tensor_q, scale, 0
        
    else:
        raise ValueError(f"Unsupported quantization type: {quant_type}")

def write_tensor_data(f, tensor_name: str, tensor: torch.Tensor, quant_type: Optional[str] = None):
    """Write a tensor to the GGUF file"""
    # Convert tensor to numpy for easier handling
    tensor_np = tensor.detach().cpu().numpy()
    
    # Get tensor type
    tensor_type = get_tensor_type(tensor, quant_type)
    
    # Apply quantization if needed
    if quant_type:
        tensor_np, scale, zero_point = quantize_tensor(tensor_np, quant_type)
    
    # Write tensor name
    encoded_name = tensor_name.encode('utf-8')
    f.write(struct.pack("<Q", len(encoded_name)))
    f.write(encoded_name)
    
    # Write tensor dimensions
    f.write(struct.pack("<I", len(tensor_np.shape)))
    for dim in tensor_np.shape:
        f.write(struct.pack("<Q", dim))
    
    # Write tensor type
    f.write(struct.pack("<I", int(tensor_type)))
    
    # Write offset (placeholder, will be updated later)
    offset_pos = f.tell()
    f.write(struct.pack("<Q", 0))  # Placeholder
    
    # Record current position to calculate actual data offset later
    return offset_pos, tensor_np, tensor_type

def validate_model_architecture(tensors: Dict[str, torch.Tensor]) -> Tuple[bool, str, Dict[str, Any]]:
    """
    Validate if the model architecture is compatible with GGUF format.
    Returns (is_valid, model_type, metadata)
    """
    # Check for common tensor patterns to identify model architecture
    tensor_names = set(tensors.keys())
    
    metadata = {
        "general.architecture": "unknown",
        "general.name": "converted_model",
        "general.source": "safetensors_to_gguf",
        "general.quantization_version": 2,
    }
    
    # Check for Llama-like models
    if any("model.embed_tokens.weight" in name for name in tensor_names):
        Logger.log("info", "Detected Llama-like architecture")
        metadata["general.architecture"] = "llama"
        return True, "llama", metadata
    
    # Check for Mistral-like models
    if any("model.norm.weight" in name for name in tensor_names) and any("lm_head.weight" in name for name in tensor_names):
        Logger.log("info", "Detected Mistral-like architecture")
        metadata["general.architecture"] = "mistral"
        return True, "mistral", metadata
    
    # Check for Falcon-like models
    if any("transformer.word_embeddings.weight" in name for name in tensor_names):
        Logger.log("info", "Detected Falcon-like architecture")
        metadata["general.architecture"] = "falcon"
        return True, "falcon", metadata
    
    # Generic transformer detection
    if any("attention" in name.lower() for name in tensor_names) and any("layer" in name.lower() for name in tensor_names):
        Logger.log("warning", "Detected generic transformer architecture, compatibility not guaranteed")
        metadata["general.architecture"] = "transformer"
        return True, "transformer", metadata
    
    # Unknown architecture
    Logger.log("warning", "Could not identify model architecture, conversion may not work correctly")
    return False, "unknown", metadata

def get_model_parameters(tensors: Dict[str, torch.Tensor]) -> Dict[str, Any]:
    """Extract model parameters from tensors"""
    params = {}
    
    # Try to determine embedding dimension
    embed_tensors = [t for name, t in tensors.items() if "embed" in name.lower() and "weight" in name.lower()]
    if embed_tensors:
        params["embedding_dim"] = embed_tensors[0].shape[1]
    
    # Try to determine vocabulary size
    vocab_tensors = [t for name, t in tensors.items() if "embed" in name.lower() and "weight" in name.lower()]
    if vocab_tensors:
        params["vocab_size"] = vocab_tensors[0].shape[0]
    
    # Try to determine number of layers
    layer_pattern = set([name.split(".")[1] for name in tensors.keys() if name.startswith("model.layers.")])
    if layer_pattern:
        params["num_layers"] = len(layer_pattern)
    
    # Try to determine number of attention heads
    for name, tensor in tensors.items():
        if "attention" in name.lower() and "weight" in name.lower() and len(tensor.shape) >= 2:
            if tensor.shape[0] % 64 == 0:  # Assuming head dimension is a multiple of 64
                params["num_attention_heads"] = tensor.shape[0] // 64
                break
    
    return params

def convert_to_gguf(input_path: str, output_path: str, quantization_type: Optional[str] = None, 
                    chunk_size: int = 1024*1024*10, metadata_extra: Optional[Dict[str, Any]] = None):
    """
    Convert a SafeTensors model to GGUF format.
    
    Args:
        input_path: Path to the input SafeTensors file
        output_path: Path to the output GGUF file
        quantization_type: Type of quantization to apply (e.g., "q4_0", "q5_1")
        chunk_size: Size of chunks to process tensors in bytes
        metadata_extra: Additional metadata to include
    """
    start_time = time.time()
    Logger.log("start", f"Starting conversion from SafeTensors to GGUF")
    Logger.log("info", f"Input: {input_path}")
    Logger.log("info", f"Output: {output_path}")
    Logger.log("info", f"Quantization: {quantization_type or 'None'}")
    
    try:
        # Load tensors from the safetensors file
        Logger.log("load", f"Loading tensors from SafeTensors file")
        tensors = load_file(input_path)
        Logger.log("info", f"Loaded {len(tensors)} tensors")
        
        # Validate model architecture
        Logger.log("validate", "Validating model architecture")
        is_valid, model_type, base_metadata = validate_model_architecture(tensors)
        if not is_valid:
            Logger.log("warning", "Model architecture validation failed, proceeding anyway")
        
        # Extract model parameters
        model_params = get_model_parameters(tensors)
        Logger.log("info", f"Detected model parameters: {model_params}")
        
        # Prepare metadata
        metadata = base_metadata.copy()
        if metadata_extra:
            metadata.update(metadata_extra)
        
        # Add model parameters to metadata
        for key, value in model_params.items():
            metadata[f"general.{key}"] = value
        
        # Log memory usage before conversion
        torch_mem_info = torch.cuda.memory_summary() if torch.cuda.is_available() else "CUDA not available"
        Logger.log("memory", f"Memory before conversion: {torch_mem_info}")
        
        # Open output file
        with open(output_path, "wb") as f:
            # Write GGUF header
            Logger.log("convert", "Writing GGUF header")
            write_gguf_header(f)
            
            # Write metadata
            Logger.log("metadata", f"Writing metadata ({len(metadata)} entries)")
            write_gguf_metadata(f, metadata)
            
            # Write number of tensors
            f.write(struct.pack("<Q", len(tensors)))
            
            # First pass: write tensor information and collect offsets
            Logger.log("tensor", "Writing tensor information")
            tensor_offsets = []
            tensor_data = []
            
            for tensor_name in Logger.progress(tensors.keys(), "Processing tensors"):
                tensor = tensors[tensor_name]
                
                # Handle unsupported types
                if tensor.dtype == torch.bfloat16:
                    Logger.log("convert", f"Converting tensor '{tensor_name}' from bfloat16 to float32")
                    tensor = tensor.to(torch.float32)
                
                # Write tensor info and get offset position
                offset_pos, tensor_np, tensor_type = write_tensor_data(f, tensor_name, tensor, quantization_type)
                tensor_offsets.append(offset_pos)
                tensor_data.append((tensor_np, tensor_type))
            
            # Second pass: write actual tensor data and update offsets
            Logger.log("save", "Writing tensor data")
            for i, (tensor_name, (tensor_np, tensor_type)) in enumerate(zip(tensors.keys(), tensor_data)):
                # Record current position as the actual data offset
                data_offset = f.tell()
                
                # Go back and update the offset
                current_pos = f.tell()
                f.seek(tensor_offsets[i])
                f.write(struct.pack("<Q", data_offset))
                f.seek(current_pos)
                
                # Write the tensor data
                f.write(tensor_np.tobytes())
                
                # Log progress for large tensors
                if tensor_np.size * tensor_np.itemsize > 1024*1024:  # If tensor is larger than 1MB
                    Logger.log("tensor", f"Wrote tensor '{tensor_name}' ({tensor_np.shape}, {tensor_np.dtype}, {tensor_type})")
        
        elapsed_time = time.time() - start_time
        Logger.log("time", f"Conversion completed in {elapsed_time:.2f} seconds")
        Logger.log("success", f"Successfully converted to '{output_path}' in GGUF format")
        
        # Log file sizes
        input_size = os.path.getsize(input_path) / (1024*1024)
        output_size = os.path.getsize(output_path) / (1024*1024)
        size_change = (output_size - input_size) / input_size * 100
        Logger.log("info", f"Input file size: {input_size:.2f} MB")
        Logger.log("info", f"Output file size: {output_size:.2f} MB")
        Logger.log("info", f"Size change: {size_change:+.2f}%")
        
        return True

    except Exception as e:
        Logger.log("error", f"Error during conversion: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    parser = argparse.ArgumentParser(description="Convert SafeTensors models to GGUF format")
    parser.add_argument("input", help="Input SafeTensors file path")
    parser.add_argument("output", help="Output GGUF file path")
    parser.add_argument("--quantize", "-q", choices=["q2_k", "q3_k", "q4_0", "q4_1", "q5_0", "q5_1", "q8_0"], 
                        help="Quantization type to apply")
    parser.add_argument("--chunk-size", type=int, default=10*1024*1024, 
                        help="Chunk size for processing large tensors (in bytes)")
    parser.add_argument("--metadata", type=str, 
                        help="Additional metadata in JSON format")
    
    args = parser.parse_args()
    
    # Parse metadata if provided
    metadata_extra = None
    if args.metadata:
        try:
            metadata_extra = json.loads(args.metadata)
        except json.JSONDecodeError:
            Logger.log("error", "Failed to parse metadata JSON")
            return 1
    
    # Run conversion
    success = convert_to_gguf(
        args.input, 
        args.output, 
        args.quantize, 
        args.chunk_size,
        metadata_extra
    )
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())