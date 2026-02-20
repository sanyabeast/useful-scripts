#![windows_subsystem = "windows"]

use std::env;
use std::ffi::OsString;
use std::fs;
use std::os::windows::ffi::OsStrExt;
use std::path::PathBuf;
use windows::core::PCWSTR;
use windows::Win32::Foundation::CloseHandle;
use windows::Win32::System::Threading::{
    CreateProcessW, CREATE_NEW_CONSOLE, PROCESS_INFORMATION, STARTUPINFOW,
};

fn main() {
    if let Err(e) = run() {
        show_error(&e);
    }
}

fn run() -> Result<(), String> {
    let exe_path = env::current_exe().map_err(|e| format!("Failed to get exe path: {}", e))?;
    let exe_dir = exe_path.parent().ok_or("Failed to get exe directory")?;
    let ini_path = exe_dir.join("affinity-launcher.ini");

    let content =
        fs::read_to_string(&ini_path).map_err(|e| format!("Failed to read affinity-launcher.ini: {}", e))?;

    let mut target_path: Option<String> = None;
    let mut threads: Vec<u32> = Vec::new();

    for line in content.lines() {
        let line = line.trim();
        if line.is_empty() || line.starts_with(';') || line.starts_with('#') {
            continue;
        }

        if let Some((key, value)) = line.split_once('=') {
            let key = key.trim().to_lowercase();
            let value = value.trim();

            match key.as_str() {
                "path" => {
                    target_path = Some(value.to_string());
                }
                "threads" => {
                    threads = value
                        .split(',')
                        .filter_map(|s| s.trim().parse::<u32>().ok())
                        .collect();
                }
                _ => {}
            }
        }
    }

    let target_path = target_path.ok_or("Missing 'path' in affinity-launcher.ini")?;
    if threads.is_empty() {
        return Err("Missing or empty 'threads' in affinity-launcher.ini".to_string());
    }

    let affinity_mask: usize = threads.iter().fold(0usize, |acc, &t| acc | (1usize << t));

    let target_exe = PathBuf::from(&target_path);
    let target_exe = if target_exe.is_absolute() {
        target_exe
    } else {
        exe_dir.join(&target_exe)
    };
    let working_dir = target_exe
        .parent()
        .map(|p| p.to_path_buf())
        .unwrap_or_else(|| exe_dir.to_path_buf());

    launch_process(&target_exe, &working_dir, affinity_mask)?;

    Ok(())
}

fn launch_process(exe_path: &PathBuf, working_dir: &PathBuf, affinity: usize) -> Result<(), String> {
    let exe_wide: Vec<u16> = exe_path.as_os_str()
        .encode_wide()
        .chain(std::iter::once(0))
        .collect();

    let dir_wide: Vec<u16> = working_dir
        .as_os_str()
        .encode_wide()
        .chain(std::iter::once(0))
        .collect();

    let mut si: STARTUPINFOW = unsafe { std::mem::zeroed() };
    si.cb = std::mem::size_of::<STARTUPINFOW>() as u32;

    let mut pi: PROCESS_INFORMATION = unsafe { std::mem::zeroed() };

    let result = unsafe {
        CreateProcessW(
            PCWSTR(exe_wide.as_ptr()),
            None,
            None,
            None,
            false,
            CREATE_NEW_CONSOLE,
            None,
            PCWSTR(dir_wide.as_ptr()),
            &si,
            &mut pi,
        )
    };

    if result.is_err() {
        return Err(format!("Failed to create process: {:?}", result));
    }

    unsafe {
        use windows::Win32::System::Threading::SetProcessAffinityMask;
        let _ = SetProcessAffinityMask(pi.hProcess, affinity);
        let _ = CloseHandle(pi.hProcess);
        let _ = CloseHandle(pi.hThread);
    }

    Ok(())
}

fn show_error(msg: &str) {
    use std::ptr::null_mut;
    let wide: Vec<u16> = OsString::from(msg)
        .encode_wide()
        .chain(std::iter::once(0))
        .collect();
    let title: Vec<u16> = OsString::from("Affinity Launcher Error")
        .encode_wide()
        .chain(std::iter::once(0))
        .collect();

    #[link(name = "user32")]
    unsafe extern "system" {
        fn MessageBoxW(hwnd: *mut (), text: *const u16, caption: *const u16, utype: u32) -> i32;
    }

    unsafe {
        MessageBoxW(null_mut(), wide.as_ptr(), title.as_ptr(), 0x10);
    }
}
