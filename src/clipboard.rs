use std::process::{ Stdio, Command };
use std::io::Write;
use std::error::Error;

/*pub fn write_windows(s: &str) -> Result<(), String> {
    let mut child = match Command::new("clip").spawn() {
        Ok(child) => child,
        Err(e) => return Err(e.description().to_string())
    };

    let stdin = match child.stdin {
        Some(ref mut stdin) =>  stdin,
        None => return Err("unable to get stdin of clip".to_string())
    };

    match stdin.write_str(s) {
        Ok(_) => Ok(()),
        Err(e) => return Err(e.description().to_string())
    }
}*/

pub fn write_linux(s: &str) -> Result<(), String> {
    match Command::new("which").arg("xclip").status() {
        Ok(status) => {
            if !status.success() {
                return Err("le-chiffre: Please install xclip!".to_string())
            }
        },

        Err(e) => return Err(e.description().to_string())
    }

    let mut child = match Command::new("xclip").args(&["-in", "-selection", "clipboard"]).stdin(Stdio::piped()).spawn() {
        Ok(child) => child,
        Err(e) => return Err(e.description().to_string())
    };

    let stdin = match child.stdin {
        Some(ref mut stdin) => stdin,
        None => return Err("unable to get stdin of xclip".to_string())
    };

    match stdin.write(s.as_bytes()) {
        Ok(_) => Ok(()),
        Err(e) => return Err(e.description().to_string())
    }
}

pub fn write_macos(s: &str) -> Result<(), String> {
    let mut child = match Command::new("pbcopy").spawn() {
        Ok(child) => child,
        Err(e) => return Err(e.description().to_string())
    };

    let stdin = match child.stdin {
        Some(ref mut stdin) =>  stdin,
        None => return Err("unable to get stdin of pbcopy".to_string())
    };

    match stdin.write(s.as_bytes()) {
        Ok(_) => Ok(()),
        Err(e) => return Err(e.description().to_string())
    }
}
