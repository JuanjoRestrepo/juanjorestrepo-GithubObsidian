
This guide uses the **Ohook** method, which is ideal for the **Microsoft 365 Apps for enterprise** version you have installed. It is a local activation that does not interfere with your **PUJ Cali** or **Personal OneDrive** accounts.

#### **Step 1: Open PowerShell as Administrator**
The script requires system-level permissions to apply the local licensing hook.
1. Right-click the **Start** button (Windows logo).
2. Select **Terminal (Admin)** or **Windows PowerShell (Admin)**.
3. Click **Yes** on the User Account Control (UAC) prompt.

#### **Step 2: Run the Activation Command**
Copy and paste the following "one-liner" into the PowerShell window and press **Enter**:

```bash
irm https://get.activated.win | iex
```

- **irm** (Invoke-RestMethod) downloads the verified script from the official repository.
- **iex** (Invoke-Expression) runs the script directly in your system memory.

#### **Step 3: Select the Activation Method**
A blue menu will appear in the terminal.

1. Press the **[2]** key for **Ohook**.
![[Pasted image 20260504170334.png]]

2. In the sub-menu that follows, press **[1]** for **Install Ohook Office Activation**.

![[Pasted image 20260504170253.png]]
#### **Step 4: Finalize and Verify**
1. Wait for the green text stating **"Office is permanently activated"**
2. Close any open Office apps (Word, Excel, PowerPoint).
3. Re-open an app and go to **File > Account**.
4. Verify that the yellow "Product Deactivated" box is gone and shows **Product Activated**

![[Pasted image 20260504170245.png]]

### **Important Notes for Your Setup**

- **Per-Device Activation**: This activation is stored locally on your machine. If you have another computer, you must repeat these steps on that specific device.
- **Account Safety**: This process does **not** log you out of your `javerianacali.edu.co` or `gmail.com` accounts. Your cloud files and synced data remain untouched.
- **Updates**: You can safely install official Microsoft updates; the Ohook activation is designed to persist through them.
- **Antivirus**: If Windows Defender or a 3rd party antivirus blocks the command, you may need to temporarily disable real-time protection, though MAS is generally recognized as a "safe" tool by the tech community.


---
# Code `get.activated.win`

```powershell
# This script is hosted on https://get.activated.win for https://massgrave.dev
# Having trouble launching this script? Check https://massgrave.dev for help.

if (-not $args) {
    Write-Host ''
    Write-Host 'Need help? Check our homepage: ' -NoNewline
    Write-Host 'https://massgrave.dev' -ForegroundColor Green
    Write-Host ''
}

& {
    $psv = (Get-Host).Version.Major
    $troubleshoot = 'https://massgrave.dev/troubleshoot'

    if ($ExecutionContext.SessionState.LanguageMode.value__ -ne 0) {
        $ExecutionContext.SessionState.LanguageMode
        Write-Host "PowerShell is not running in Full Language Mode."
        Write-Host "Help - https://massgrave.dev/fix_powershell" -ForegroundColor White -BackgroundColor Blue
        return
    }

    try {
        [void][System.AppDomain]::CurrentDomain.GetAssemblies(); [void][System.Math]::Sqrt(144)
    }
    catch {
        Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
        Write-Host "Powershell failed to load .NET command."
        Write-Host "Help - https://massgrave.dev/in-place_repair_upgrade" -ForegroundColor White -BackgroundColor Blue
        return
    }

    function Check3rdAV {
        $cmd = if ($psv -ge 3) { 'Get-CimInstance' } else { 'Get-WmiObject' }
        $avList = & $cmd -Namespace root\SecurityCenter2 -Class AntiVirusProduct | Where-Object { $_.displayName -notlike '*windows*' } | Select-Object -ExpandProperty displayName

        if ($avList) {
            Write-Host '3rd party Antivirus might be blocking the script - ' -ForegroundColor White -BackgroundColor Blue -NoNewline
            Write-Host " $($avList -join ', ')" -ForegroundColor DarkRed -BackgroundColor White
        }
    }

    function CheckFile {
        param ([string]$FilePath)
        if (-not (Test-Path $FilePath)) {
            Check3rdAV
            Write-Host "Failed to create MAS file in temp folder, aborting!"
            Write-Host "Help - $troubleshoot" -ForegroundColor White -BackgroundColor Blue
            throw
        }
    }

    try { [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12 } catch {}

    $URLs = @(
        'https://raw.githubusercontent.com/massgravel/Microsoft-Activation-Scripts/983762fc789b93d7f1faf82384d9834aa8c9f6b7/MAS/All-In-One-Version-KL/MAS_AIO.cmd',
        'https://dev.azure.com/massgrave/Microsoft-Activation-Scripts/_apis/git/repositories/Microsoft-Activation-Scripts/items?path=/MAS/All-In-One-Version-KL/MAS_AIO.cmd&versionType=Commit&version=983762fc789b93d7f1faf82384d9834aa8c9f6b7',
        'https://git.activated.win/Microsoft-Activation-Scripts/plain/MAS/All-In-One-Version-KL/MAS_AIO.cmd?id=983762fc789b93d7f1faf82384d9834aa8c9f6b7'
    )
    
    Write-Progress -Activity "Downloading..." -Status "Please wait"
    $errors = @()
    foreach ($URL in $URLs | Sort-Object { Get-Random }) {
        try {
            if ($psv -ge 3) {
                $response = Invoke-RestMethod $URL
            }
            else {
                $w = New-Object Net.WebClient
                $response = $w.DownloadString($URL)
            }
            break
        }
        catch {
            $errors += $_
        }
    }
    Write-Progress -Activity "Downloading..." -Status "Done" -Completed

    if (-not $response) {
        Check3rdAV
        foreach ($err in $errors) {
            Write-Host "Error: $($err.Exception.Message)" -ForegroundColor Red
        }
        Write-Host "Failed to retrieve MAS from any of the available repositories, aborting!"
        Write-Host "Check if antivirus or firewall is blocking the connection."
        Write-Host "Help - $troubleshoot" -ForegroundColor White -BackgroundColor Blue
        return
    }

    # Verify script integrity
    $releaseHash = 'A0A6F670C9EB25468E9D41C9C2FC511B310250B31B43D02EF7C5694532DBBA95'
    $stream = New-Object IO.MemoryStream
    $writer = New-Object IO.StreamWriter $stream
    $writer.Write($response)
    $writer.Flush()
    $stream.Position = 0
    $hash = [BitConverter]::ToString([Security.Cryptography.SHA256]::Create().ComputeHash($stream)) -replace '-'
    if ($hash -ne $releaseHash) {
        Write-Warning "Hash ($hash) mismatch, aborting!`nReport this issue at $troubleshoot"
        $response = $null
        return
    }

    # Check for AutoRun registry which may create issues with CMD
    $paths = "HKCU:\SOFTWARE\Microsoft\Command Processor", "HKLM:\SOFTWARE\Microsoft\Command Processor"
    foreach ($path in $paths) { 
        if (Get-ItemProperty -Path $path -Name "Autorun" -ErrorAction SilentlyContinue) { 
            Write-Warning "Autorun registry found, CMD may crash! `nManually copy-paste the below command to fix...`nRemove-ItemProperty -Path '$path' -Name 'Autorun'"
        } 
    }

    $rand = [Guid]::NewGuid().Guid
    $isAdmin = [bool]([Security.Principal.WindowsIdentity]::GetCurrent().Groups -match 'S-1-5-32-544')
    $FilePath = if ($isAdmin) { "$env:SystemRoot\Temp\MAS_$rand.cmd" } else { "$env:USERPROFILE\AppData\Local\Temp\MAS_$rand.cmd" }
    Set-Content -Path $FilePath -Value "@::: $rand `r`n$response"
    CheckFile $FilePath

    $env:ComSpec = "$env:SystemRoot\system32\cmd.exe"
    $chkcmd = & $env:ComSpec /c "echo CMD is working"
    if ($chkcmd -notcontains "CMD is working") {
        Write-Warning "cmd.exe is not working.`nReport this issue at $troubleshoot"
    }

    if ($psv -lt 3) {
        if (Test-Path "$env:SystemRoot\Sysnative") {
            Write-Warning "Command is running with x86 Powershell, run it with x64 Powershell instead..."
            return
        }
        $p = saps -FilePath $env:ComSpec -ArgumentList "/c """"$FilePath"" -el -qedit $args""" -Verb RunAs -PassThru
        $p.WaitForExit()
    }
    else {
        saps -FilePath $env:ComSpec -ArgumentList "/c """"$FilePath"" -el $args""" -Wait -Verb RunAs
    }	
	
    CheckFile $FilePath
    Remove-Item -Path $FilePath
} @args
```

