/************************************************************
 * validUrl.js
 ************************************************************/

// Dépendances Playwright + Crypto
const { createCipheriv } = require("crypto");
const { devices, chromium } = require("playwright");

// Utils.js fusionné
class Utils {
  static getRandomInt(a, b) {
    const min = Math.min(a, b);
    const max = Math.max(a, b);
    const diff = max - min + 1;
    return min + Math.floor(Math.random() * Math.floor(diff));
  }

  static generateVerifyFp() {
    return 'verify_5b161567bda98b6a50c0414d99909d4b';
  }
}

// Classe Signer
class Signer {
  constructor(default_url, userAgent, browser) {
    this.userAgent =
      userAgent ||
      "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.109 Safari/537.36";

    this.args = [
      "--disable-blink-features",
      "--disable-blink-features=AutomationControlled",
      "--disable-infobars",
      "--window-size=1920,1080",
      "--start-maximized",
      `--user-agent="${this.userAgent}"`,
    ];

    this.default_url = default_url || "https://www.tiktok.com/@rihanna?lang=en";
    this.password = "webapp1.0+202106";
    if (browser) {
      this.browser = browser;
      this.isExternalBrowser = true;
    }

    this.options = {
      headless: true,
      args: this.args,
      ignoreDefaultArgs: ["--mute-audio", "--hide-scrollbars"],
      ignoreHTTPSErrors: true,
    };
  }

  async init() {
    if (!this.browser) {
      this.browser = await chromium.launch(this.options);
    }
    const iPhone11 = devices["iPhone 11 Pro"];
    let emulateTemplate = {
      ...iPhone11,
      locale: "en-US",
      deviceScaleFactor: Utils.getRandomInt(1, 3),
      isMobile: Math.random() > 0.5,
      hasTouch: Math.random() > 0.5,
      userAgent: this.userAgent,
    };
    emulateTemplate.viewport.width = Utils.getRandomInt(320, 1920);
    emulateTemplate.viewport.height = Utils.getRandomInt(320, 1920);

    this.context = await this.browser.newContext({
      bypassCSP: true,
      ...emulateTemplate,
    });
    this.page = await this.context.newPage();

    await this.page.route("**/*", (route) => {
      return route.request().resourceType() === "script"
        ? route.abort()
        : route.continue();
    });

    await this.page.goto(this.default_url, {
      waitUntil: "networkidle",
    });

    const LOAD_SCRIPTS = ["signer.js", "webmssdk.js", "xbogus.js"];
    const fs = require('fs');
    for (const script of LOAD_SCRIPTS) {
      const scriptPath = `${__dirname}/javascript/${script}`;
      if (!fs.existsSync(scriptPath)) {
        console.error(`Erreur : Le fichier ${scriptPath} n'existe pas`);
        throw new Error(`Le fichier ${script} est manquant`);
      }
      await this.page.addScriptTag({
        path: scriptPath,
      });
    }

    await this.page.evaluate(() => {
      window.generateSignature = function generateSignature(url) {
        if (typeof window.byted_acrawler?.sign !== "function") {
          throw "No signature function found";
        }
        return window.byted_acrawler.sign({ url: url });
      };

      if (typeof window.generateBogus !== "function") {
        throw new Error("No X-Bogus function found (window.generateBogus is missing).");
      }
    });
  }

  async navigator() {
    return await this.page.evaluate(() => {
      return {
        deviceScaleFactor: window.devicePixelRatio,
        user_agent: window.navigator.userAgent,
        browser_language: window.navigator.language,
        browser_platform: window.navigator.platform,
        browser_name: window.navigator.appCodeName,
        browser_version: window.navigator.appVersion,
      };
    });
  }

  async sign(link) {
    let verify_fp = Utils.generateVerifyFp();
    let newUrl = link + "&verifyFp=" + verify_fp;

    let token = await this.page.evaluate(`generateSignature("${newUrl}")`);
    let signed_url = newUrl + "&_signature=" + token;

    let queryString = new URL(signed_url).searchParams.toString();

    let bogus = await this.page.evaluate(`generateBogus("${queryString}","${this.userAgent}")`);
    signed_url += "&X-Bogus=" + bogus;

    return {
      signature: token,
      verify_fp: verify_fp,
      signed_url: signed_url,
      "x-tt-params": this.xttparams(queryString),
      "x-bogus": bogus,
    };
  }

  xttparams(query_str) {
    query_str += "&is_encryption=1";
    const cipher = createCipheriv("aes-128-cbc", this.password, this.password);
    return Buffer.concat([cipher.update(query_str), cipher.final()]).toString("base64");
  }

  async close() {
    if (this.browser && !this.isExternalBrowser) {
      await this.browser.close();
      this.browser = null;
    }
    if (this.page) {
      this.page = null;
    }
  }
}

// Code principal
(async function main() {
  const url = process.argv[2];
  if (!url) {
    console.error("Veuillez spécifier une URL en paramètre, ex : node validUrl.js https://www.tiktok.com/...");
    process.exit(1);
  }

  try {
    const signer = new Signer();
    await signer.init();
    const sign = await signer.sign(url);
    const navigatorInfo = await signer.navigator();
    let output = JSON.stringify({
      status: "ok",
      data: {
        ...sign,
        navigator: navigatorInfo,
      },
    });
    console.log(output);
    await signer.close();
  } catch (err) {
    console.error('Erreur dans validUrl.js:', err);
    let output = JSON.stringify({
      status: "error",
      error: err.message,
    });
    console.log(output);
    process.exit(1);
  }
})();