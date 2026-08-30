// Nobleparc — PayPal IPN Webhook
// Deploy: npx wrangler deploy cloudflare-worker.js --name nobleparc-ipn
// Then set PayPal IPN URL to: https://nobleparc-ipn.YOUR-SUBDOMAIN.workers.dev

const SHEET_SCRIPT_URL = 'https://script.google.com/macros/s/YOUR_SCRIPT_ID/exec'
const PAYPAL_BUSINESS_EMAIL = 'info@nobleparc.com'
const INVALID_STATES = ['HI', 'AK', 'PR', 'GU', 'VI', 'AS', 'MP']
const ALLOWED_COUNTRY = 'US'

export default {
  async fetch(request) {
    // Only accept POST from PayPal IPN
    if (request.method !== 'POST') {
      return new Response('OK', { status: 200 })
    }

    try {
      const formData = await request.formData()
      const paymentStatus = formData.get('payment_status')
      const receiverEmail = formData.get('receiver_email')

      // Ignore non-completed payments and wrong receiver
      if (paymentStatus !== 'Completed') {
        return new Response('OK', { status: 200 })
      }
      if (receiverEmail !== PAYPAL_BUSINESS_EMAIL) {
        return new Response('OK', { status: 200 })
      }

      // Extract customer data
      const firstName = formData.get('first_name') || ''
      const lastName = formData.get('last_name') || ''
      const payerEmail = formData.get('payer_email') || ''
      const itemName = formData.get('item_name') || ''
      const gross = formData.get('mc_gross') || '0'
      const currency = formData.get('mc_currency') || 'USD'
      const txnId = formData.get('txn_id') || ''
      const street = formData.get('address_street') || ''
      const city = formData.get('address_city') || ''
      const state = formData.get('address_state') || ''
      const zip = formData.get('address_zip') || ''
      const country = formData.get('address_country_code') || ''
      const phone = formData.get('contact_phone') || ''

      // Validate mainland USA
      const isMainland = country === ALLOWED_COUNTRY && !INVALID_STATES.includes(state)
      const customerName = `${firstName} ${lastName}`.trim()
      const shipping = `${street}, ${city}, ${state} ${zip}`.trim()

      // Build order object
      const order = {
        timestamp: new Date().toISOString(),
        date: new Date().toISOString().split('T')[0],
        customer_name: customerName,
        customer_email: payerEmail,
        customer_phone: phone,
        product: itemName,
        price: gross,
        currency: currency,
        paypal_txn: txnId,
        shipping: shipping,
        state: state,
        country: country,
        is_mainland: isMainland ? 'YES' : 'NO',
        status: isMainland 
          ? '🟡 Payment received — pending review' 
          : '🟡 NON-MAINLAND — manual review required',
        blind_shipping_note: '⚠️ BLIND SHIPPING: No invoice, no promotional material, no Chinese writing. Neutral packaging only. Do not include any supplier branding or documents.',
        notes: isMainland ? '' : '⚠️ Outside continental US — manual review and possible refund required'
      }

      // Send to Google Sheet via Apps Script
      const sheetResponse = await fetch(SHEET_SCRIPT_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(order)
      })

      // Log for Cloudflare dashboard
      console.log(`Order received: ${txnId} — ${itemName} — $${gross} — ${customerName} — ${state}`)

      return new Response('OK', { status: 200 })
    } catch (err) {
      console.error('IPN Error:', err.message)
      return new Response('OK', { status: 200 })
    }
  }
}