// Nobleparc — PayPal IPN Webhook
// Deploy: npx wrangler deploy index.js --name nobleparc-ipn
// PayPal IPN URL: https://nobleparc-ipn.YOUR-SUBDOMAIN.workers.dev

const SHEET_SCRIPT_URL = 'https://script.google.com/macros/s/YOUR_SCRIPT_ID/exec'
const PAYPAL_BUSINESS_EMAIL = 'info@nobleparc.com'
const INVALID_STATES = ['HI', 'AK', 'PR', 'GU', 'VI', 'AS', 'MP']
const ALLOWED_COUNTRY = 'US'

let orderCounter = 0

function generateOrderID(dateStr) {
  const date = dateStr || new Date().toISOString().split('T')[0].replace(/-/g, '')
  orderCounter++
  const seq = String(orderCounter).padStart(3, '0')
  return `NP-${date}-${seq}`
}

export default {
  async fetch(request) {
    if (request.method !== 'POST') {
      return new Response('OK', { status: 200 })
    }

    try {
      const formData = await request.formData()
      const paymentStatus = formData.get('payment_status')
      const receiverEmail = formData.get('receiver_email')

      if (paymentStatus !== 'Completed') return new Response('OK', { status: 200 })
      if (receiverEmail !== PAYPAL_BUSINESS_EMAIL) return new Response('OK', { status: 200 })

      const firstName = formData.get('first_name') || ''
      const lastName = formData.get('last_name') || ''
      const payerEmail = formData.get('payer_email') || ''
      const itemName = formData.get('item_name') || ''
      const gross = formData.get('mc_gross') || '0'
      const txnId = formData.get('txn_id') || ''
      const street = formData.get('address_street') || ''
      const street2 = formData.get('address_street2') || ''
      const city = formData.get('address_city') || ''
      const state = formData.get('address_state') || ''
      const zip = formData.get('address_zip') || ''
      const country = formData.get('address_country_code') || ''
      const phone = formData.get('contact_phone') || ''
      const payerStatus = formData.get('payer_status') || ''
      const paymentDate = formData.get('payment_date') || ''
      const paymentType = formData.get('payment_type') || ''

      const isMainland = country === ALLOWED_COUNTRY && !INVALID_STATES.includes(state)
      const customerName = `${firstName} ${lastName}`.trim()
      const orderId = generateOrderID()

      // Build row for the 30-column sheet (A–AD)
      const row = [
        orderId,                                          // A: Order ID
        new Date().toISOString().replace('T', ' ').slice(0, 16), // B: Date (YYYY-MM-DD HH:MM)
        txnId,                                            // C: PayPal Transaction ID
        customerName,                                     // D: Customer Name
        payerEmail,                                       // E: Email
        phone,                                            // F: Phone
        street,                                           // G: Address Line 1
        street2,                                          // H: Address Line 2
        city,                                             // I: City
        state,                                            // J: State
        zip,                                              // K: ZIP
        isMainland ? 'OK' : 'BLOCKED',                    // L: Mainland Check
        itemName,                                         // M: Product
        parseFloat(gross),                                // N: Selling Price
        '',                                               // O: PayPal Fee (formula in sheet)
        '',                                               // P: Product Cost (manual)
        '',                                               // Q: Shipping Cost (manual)
        '',                                               // R: Total Cost (formula in sheet)
        '',                                               // S: Margin (formula in sheet)
        isMainland ? 'Bozza' : 'Problema',                // T: Status
        isMainland ? 'Pending' : 'Rejected',              // U: Human Validation
        '',                                               // V: Validated By
        '',                                               // W: Validation Date
        '',                                               // X: CJ Order ID
        '',                                               // Y: Tracking Number
        '',                                               // Z: Carrier
        'Yes',                                            // AA: Blind Note Added
        '',                                               // AB: Traffic Source
        isMainland ? '' : 'BLOCKED: outside continental US', // AC: Notes
        new Date().toISOString().replace('T', ' ').slice(0, 16) // AD: Last Update
      ]

      await fetch(SHEET_SCRIPT_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ row: row, sheetName: 'Nobleparc – Orders Control' })
      })

      console.log(`Order: ${orderId} | ${itemName} | $${gross} | ${customerName} | ${state} | ${isMainland ? 'OK' : 'BLOCKED'}`)

      return new Response('OK', { status: 200 })
    } catch (err) {
      console.error('IPN Error:', err.message)
      return new Response('OK', { status: 200 })
    }
  }
}