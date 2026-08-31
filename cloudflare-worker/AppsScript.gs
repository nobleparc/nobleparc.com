// Nobleparc — Order Fulfillment Google Apps Script
// Deploy: Extensions → Apps Script → paste this → Deploy → Web App
// Execute as: Me → Who has access: Anyone
// Copy the Web App URL → paste into cloudflare-worker/index.js as SHEET_SCRIPT_URL

const SHEET_ID = 'YOUR_GOOGLE_SHEET_ID'  // Replace with your sheet ID
const SHEET_NAME = 'Nobleparc – Orders Control'

function doPost(e) {
  try {
    const data = JSON.parse(e.postData.contents)
    const ss = SpreadsheetApp.openById(SHEET_ID)
    const sheet = ss.getSheetByName(SHEET_NAME)
    if (!sheet) throw new Error(`Sheet "${SHEET_NAME}" not found`)

    // Ensure headers exist on first run
    if (sheet.getLastRow() === 0) {
      sheet.appendRow([
        'Order ID', 'Date', 'PayPal Transaction ID', 'Customer Name', 'Email',
        'Phone', 'Address Line 1', 'Address Line 2', 'City', 'State', 'ZIP',
        'Mainland Check', 'Product', 'Selling Price', 'PayPal Fee',
        'Product Cost', 'Shipping Cost', 'Total Cost', 'Margin',
        'Status', 'Human Validation', 'Validated By', 'Validation Date',
        'CJ Order ID', 'Tracking Number', 'Carrier', 'Blind Note Added',
        'Traffic Source', 'Notes', 'Last Update'
      ])
      sheet.setFrozenRows(1)
    }

    sheet.appendRow(data.row)

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

function doGet() {
  return ContentService
    .createTextOutput(JSON.stringify({ status: 'OK', message: 'Nobleparc IPN Web App is running' }))
    .setMimeType(ContentService.MimeType.JSON)
}