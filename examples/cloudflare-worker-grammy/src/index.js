/**
 * Cloudflare Worker example for Telegram Bot API 10.4 + Mini App initData verification.
 * Uses JSDoc type annotations for full TypeScript / Wrangler checking.
 *
 * Official Sources:
 * - https://core.telegram.org/bots/api
 * - https://core.telegram.org/bots/widgets
 * - https://core.telegram.org/bots/webapps#validating-data-received-via-the-mini-app
 */

import { Bot } from "grammy";

/**
 * @param {string} a
 * @param {string} b
 * @returns {boolean}
 */
function timingSafeEqual(a, b) {
  const enc = new TextEncoder();
  const aBytes = enc.encode(a);
  const bBytes = enc.encode(b);
  if (aBytes.byteLength !== bBytes.byteLength) return false;
  let diff = 0;
  for (let i = 0; i < aBytes.byteLength; i++) {
    diff |= aBytes[i] ^ bBytes[i];
  }
  return diff === 0;
}

/**
 * Validates Telegram.WebApp.initData using Web Crypto HMAC-SHA256.
 * @param {string} initDataRaw
 * @param {string} botToken
 * @returns {Promise<boolean>}
 */
export async function verifyMiniAppInitData(initDataRaw, botToken) {
  const params = new URLSearchParams(initDataRaw);
  const hash = params.get("hash");
  if (!hash) return false;
  params.delete("hash");

  const entries = Array.from(params.entries()).sort(([a], [b]) => a.localeCompare(b));
  const dataCheckString = entries.map(([k, v]) => `${k}=${v}`).join("\n");

  const enc = new TextEncoder();
  const webAppDataKey = await crypto.subtle.importKey(
    "raw",
    enc.encode("WebAppData"),
    { name: "HMAC", hash: "SHA-256" },
    false,
    ["sign"]
  );
  const secretKeyBytes = await crypto.subtle.sign("HMAC", webAppDataKey, enc.encode(botToken));
  const secretKey = await crypto.subtle.importKey(
    "raw",
    secretKeyBytes,
    { name: "HMAC", hash: "SHA-256" },
    false,
    ["sign"]
  );
  const sigBytes = new Uint8Array(await crypto.subtle.sign("HMAC", secretKey, enc.encode(dataCheckString)));
  const computedHex = Array.from(sigBytes).map((b) => b.toString(16).padStart(2, "0")).join("");
  return timingSafeEqual(computedHex, hash);
}

export default {
  /**
   * @param {Request} request
   * @param {{ BOT_TOKEN: string, WEBHOOK_SECRET: string }} env
   * @param {ExecutionContext} ctx
   */
  async fetch(request, env, ctx) {
    const url = new URL(request.url);

    if (url.pathname === "/api/verify-init-data" && request.method === "POST") {
      const body = await request.json();
      if (!body.initData || !(await verifyMiniAppInitData(body.initData, env.BOT_TOKEN))) {
        return Response.json({ ok: false, error: "Invalid initData signature" }, { status: 401 });
      }
      return Response.json({ ok: true });
    }

    if (request.method !== "POST") {
      return new Response("OK", { status: 200 });
    }

    const headerSecret = request.headers.get("X-Telegram-Bot-Api-Secret-Token") ?? "";
    if (!timingSafeEqual(headerSecret, env.WEBHOOK_SECRET)) {
      return new Response("Unauthorized", { status: 401 });
    }

    const bot = new Bot(env.BOT_TOKEN);
    const update = await request.json();

    ctx.waitUntil(
      (async () => {
        if (update.widget_query) {
          const wq = update.widget_query;
          await bot.api.raw.answerWidgetQuery({
            widget_query_id: wq.id,
            data: JSON.stringify({ status: "acknowledged", timestamp: Date.now() }),
            ephemeral_message: {
              text: "✅ Widget action recorded (visible only to you)!",
            },
          });
          return;
        }

        if (update.message?.text === "/widget") {
          await bot.api.raw.sendWidget({
            chat_id: update.message.chat.id,
            url: "https://widgets.example.com/status-card",
            aspect_ratio: "16:9",
            data: JSON.stringify({ step: 1, label: "Live Widget" }),
          });
          return;
        }

        if (update.message?.text === "/stars") {
          await bot.api.sendInvoice(
            update.message.chat.id,
            "Pro Pass",
            "Unlock Pro features for 30 days with Telegram Stars",
            "pro_pass_30d",
            "XTR",
            [{ label: "Pro Pass", amount: 50 }]
          );
          return;
        }

        if (update.pre_checkout_query) {
          await bot.api.answerPreCheckoutQuery(update.pre_checkout_query.id, true);
        }
      })()
    );

    return new Response("OK", { status: 200 });
  },
};
