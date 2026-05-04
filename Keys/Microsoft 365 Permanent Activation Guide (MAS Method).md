
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
