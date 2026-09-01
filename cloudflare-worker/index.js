// Nobleparc — PayPal IPN Webhook (SECURE version)
// Paste this into: Cloudflare Dashboard → Workers & Pages → nobleparc-ipn → Edit code
// Handles BOTH application/json AND application/x-www-form-urlencoded (PayPal IPN standard)

const SHEET_SCRIPT_URL = 'YOUR_GOOGLE_APPS_SCRIPT_URL_HERE' // ← YOUR Web App URL (https://script.google.com/macros/s/.../exec)
const PAYPAL_BUSINESS_EMAIL = 'info@nobleparc.com'
const INVALID_STATES = ['HI', 'AK', 'PR', 'GU', 'VI', 'AS', 'MP']
const ALLOWED_COUNTRY = 'US'

let orderCounter = 0

function generateOrderID() {
  const now = new Date()
  const date = now.toISOString().split('T')[0].replace(/-/g, '')
  orderCounter++
  const seq = String(orderCounter).padStart(3, '0')
  return `NP-${date}-${seq}`
}

function formatDateTime(d) {
  const pad = (n) => String(n).padStart(2, '0')
  return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())} ${pad(d.getHours())}:${pad(d.getMinutes())}`
}

async function parsePayload(request) {
  const contentType = request.headers.get('Content-Type') || ''
  if (contentType.includes('application/json')) {
    return await request.json()
  }
  // Default: form-urlencoded (PayPal IPN standard)
  const formData = await request.formData()
  const obj = {}
  for (const [key, value] of formData.entries()) {
    obj[key] = value
  }
  return obj
}

export default {
  async fetch(request) {
    // Only accept POST (PayPal IPN sends POST)
    if (request.method !== 'POST') {
      return new Response('OK', { status: 200 })
    }

    try {
      const p = await parsePayload(request)

      // === SECURITY CHECK 1: Payment must be Completed ===
      if (p.payment_status !== 'Completed') {
        console.log(`IPN ignored: status=${p.payment_status} (not Completed)`)
        return new Response('OK', { status: 200 }) // silently drop, NO sheet write
      }

      // === SECURITY CHECK 2: Receiver must be info@nobleparc.com ===
      if (p.receiver_email !== PAYPAL_BUSINESS_EMAIL) {
        console.log(`IPN ignored: receiver=${p.receiver_email} (not our business email)`)
        return new Response('OK', { status: 200 }) // silently drop, NO sheet write
      }

      // Extract fields
      const firstName = p.first_name || ''
      const lastName = p.last_name || ''
      const customerName = `${firstName} ${lastName}`.trim()
      const txnId = p.txn_id || ''
      const gross = parseFloat(p.mc_gross) || 0
      const state = p.address_state || ''
      const country = p.address_country_code || ''

      // === MAINLAND USA CHECK ===
      const isMainland = country === ALLOWED_COUNTRY && !INVALID_STATES.includes(state)

      const orderId = generateOrderID()
      const dateTime = formatDateTime(new Date())

      // Build row for the 30-column sheet (A–AD)
      const row = [
        orderId,                                  // A: Order ID
        dateTime,                                 // B: Date (YYYY-MM-DD HH:MM)
        txnId,                                    // C: PayPal Transaction ID
        customerName,                             // D: Customer Name
        p.payer_email || '',                      // E: Email
        p.contact_phone || '',                    // F: Phone
        p.address_street || '',                   // G: Address Line 1
        p.address_street2 || '',                  // H: Address Line 2
        p.address_city || '',                     // I: City
        state,                                    // J: State
        p.address_zip || '',                      // K: ZIP
        isMainland ? 'OK' : 'BLOCKED',            // L: Mainland Check
        p.item_name || '',                        // M: Product
        gross,                                    // N: Selling Price
        '',                                       // O: PayPal Fee (formula in sheet)
        '',                                       // P: Product Cost (manual)
        '',                                       // Q: Shipping Cost (manual)
        '',                                       // R: Total Cost (formula in sheet)
        '',                                       // S: Margin (formula in sheet)
        isMainland ? 'Bozza' : 'Problema',        // T: Status
        isMainland ? 'Pending' : 'Rejected',      // U: Human Validation
        '',                                       // V: Validated By
        '',                                       // W: Validation Date
        '',                                       // X: CJ Order ID
        '',                                       // Y: Tracking Number
        '',                                       // Z: Carrier
        'Yes',                                    // AA: Blind Note Added
        '',                                       // AB: Traffic Source
        isMainland ? '' : 'BLOCKED: outside continental US', // AC: Notes
        dateTime                                  // AD: Last Update
      ]

      // Send to Google Sheet via Apps Script
      const sheetResponse = await fetch(SHEET_SCRIPT_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ row: row, sheetName: 'Nobleparc – Orders Control' })
      })

      const sheetText = await sheetResponse.text()
      console.log(`Order: ${orderId} | ${p.item_name} | $${gross} | ${customerName} | ${state} | ${isMainland ? 'OK' : 'BLOCKED'} | Sheet: ${sheetText}`)

      return new Response('OK', { status: 200 })

    } catch (err) {
      console.error('IPN Error:', err.message)
      return new Response('OK', { status: 200 })
    }
  }
}