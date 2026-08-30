// Nobleparc — Order Fulfillment Google Apps Script
// Deploy as Web App:
//   1. Open https://script.google.com/
//   2. Create new project → paste this code
//   3. Deploy → New deployment → Web App
//   4. Execute as: Me → Who has access: Anyone
//   5. Copy the Web App URL → paste into cloudflare-worker/index.js as SHEET_SCRIPT_URL

// === CONFIGURATION ===
const SHEET_ID = 'YOUR_GOOGLE_SHEET_ID'  // Replace with your sheet ID
const ORDERS_SHEET_NAME = 'Orders'
const FINANCE_SHEET_NAME = 'Finance'

// === DO POST — Receive order from Cloudflare Worker ===
function doPost(e) {
  try {
    const data = JSON.parse(e.postData.contents)
    const ss = SpreadsheetApp.openById(SHEET_ID)
    
    // --- Write to Orders sheet ---
    const ordersSheet = ss.getSheetByName(ORDERS_SHEET_NAME)
    if (!ordersSheet) {
      throw new Error(`Sheet "${ORDERS_SHEET_NAME}" not found`)
    }
    
    // Ensure headers exist
    if (ordersSheet.getLastRow() === 0) {
      ordersSheet.appendRow([
        'Timestamp', 'Date', 'Customer Name', 'Customer Email', 'Phone',
        'Product', 'Price', 'Currency', 'PayPal TXN',
        'Shipping Address', 'State', 'Country', 'Mainland USA',
        'Status', 'CJ Order #', 'Tracking #', 'Customer Notified',
        'Blind Shipping Note', 'Notes'
      ])
    }
    
    ordersSheet.appendRow([
      data.timestamp || '',
      data.date || '',
      data.customer_name || '',
      data.customer_email || '',
      data.customer_phone || '',
      data.product || '',
      data.price || '',
      data.currency || '',
      data.paypal_txn || '',
      data.shipping || '',
      data.state || '',
      data.country || '',
      data.is_mainland || '',
      data.status || '',
      '',  // CJ Order #
      '',  // Tracking #
      'NO', // Customer Notified
      data.blind_shipping_note || '',
      data.notes || ''
    ])
    
    // --- Update Finance tab ---
    const financeSheet = ss.getSheetByName(FINANCE_SHEET_NAME)
    if (financeSheet) {
      // Auto-calculate net after PayPal fees (2.99% + $0.49)
      const gross = parseFloat(data.price) || 0
      const paypalFee = gross * 0.0299 + 0.49
      const net = gross - paypalFee
      
      financeSheet.appendRow([
        data.date || '',
        data.paypal_txn || '',
        data.product || '',
        gross,
        paypalFee.toFixed(2),
        net.toFixed(2),
        '',  // CJ Cost (to be filled manually)
        '',  // Net after CJ (to be calculated)
        data.customer_email || '',
        data.state || ''
      ])
    }
    
    return ContentService
      .createTextOutput(JSON.stringify({ success: true }))
      .setMimeType(ContentService.MimeType.JSON)
      
  } catch (err) {
    console.error('Apps Script Error:', err.message)
    return ContentService
      .createTextOutput(JSON.stringify({ success: false, error: err.message }))
      .setMimeType(ContentService.MimeType.JSON)
  }
}

// === DO GET — Health check ===
function doGet() {
  return ContentService
    .createTextOutput(JSON.stringify({ status: 'OK', message: 'Nobleparc IPN Web App is running' }))
    .setMimeType(ContentService.MimeType.JSON)
}

// === Setup — Create initial sheets with headers ===
function setupSheet() {
  const ss = SpreadsheetApp.openById(SHEET_ID)
  
  // Create Orders sheet
  let sheet = ss.getSheetByName(ORDERS_SHEET_NAME)
  if (!sheet) {
    sheet = ss.insertSheet(ORDERS_SHEET_NAME)
  }
  sheet.getRange(1, 1, 1, 19).setValues([[
    'Timestamp', 'Date', 'Customer Name', 'Customer Email', 'Phone',
    'Product', 'Price', 'Currency', 'PayPal TXN',
    'Shipping Address', 'State', 'Country', 'Mainland USA',
    'Status', 'CJ Order #', 'Tracking #', 'Customer Notified',
    'Blind Shipping Note', 'Notes'
  ]])
  sheet.setFrozenRows(1)
  
  // Create Finance sheet
  let finance = ss.getSheetByName(FINANCE_SHEET_NAME)
  if (!finance) {
    finance = ss.insertSheet(FINANCE_SHEET_NAME)
  }
  finance.getRange(1, 1, 1, 10).setValues([[
    'Date', 'PayPal TXN', 'Product', 'Gross ($)', 
    'PayPal Fee ($)', 'Net ($)', 'CJ Cost ($)', 
    'Net After CJ ($)', 'Customer Email', 'State'
  ]])
  finance.setFrozenRows(1)
  
  // Add data validation for Status column
  const statusRange = sheet.getRange('N2:N')
  const rule = SpreadsheetApp.newDataValidation()
    .requireValueInList([
      '🟡 Payment received — pending review',
      '🟢 Address verified — sent to CJ',
      '🔵 Tracking received — customer notified',
      '⚪ Delivered',
      '🔴 Refund issued'
    ], true)
    .build()
  statusRange.setDataValidation(rule)
  
  // Format columns
  sheet.setColumnWidths(1, 19, 120)
  finance.setColumnWidths(1, 10, 120)
}