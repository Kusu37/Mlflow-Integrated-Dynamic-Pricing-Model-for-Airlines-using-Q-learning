function saveOwnerProfile() {
    // Get owner profile data
    const ownerName = document.getElementById('owner-name').value;
    const ownerEmail = document.getElementById('owner-email').value;
    const ownerPhone = document.getElementById('owner-phone').value;

    // Here you can send the data to the server (if needed)
    console.log('Owner Profile Saved:', ownerName, ownerEmail, ownerPhone);
}

function addRevenue() {
    const ticketRevenue = parseFloat(document.getElementById('ticket-revenue').value) || 0;
    const extraRevenue = parseFloat(document.getElementById('extra-revenue').value) || 0;
    const loyaltyRevenue = parseFloat(document.getElementById('loyalty-revenue').value) || 0;

    const totalRevenue = ticketRevenue + extraRevenue + loyaltyRevenue;
    document.getElementById('total-revenue').textContent = `$${totalRevenue.toFixed(2)}`;
}

function addExpense() {
    const maintenanceExpense = parseFloat(document.getElementById('maintenance-expense').value) || 0;
    const staffExpense = parseFloat(document.getElementById('staff-expense').value) || 0;
    const airportFee = parseFloat(document.getElementById('airport-fee').value) || 0;

    const totalExpenses = maintenanceExpense + staffExpense + airportFee;
    document.getElementById('total-expenses').textContent = `$${totalExpenses.toFixed(2)}`;
}

function analyzeRevenueExpense() {
    // Simulate revenue and expense analysis
    const analysis = "Revenue and Expense Analysis: Net Profit/Loss calculation.";
    document.getElementById('analytics-results').textContent = analysis;
}

function setDynamicPricing() {
    const basePrice = parseFloat(document.getElementById('base-price').value) || 0;
    const pricingFactor = parseFloat(document.getElementById('pricing-factor').value) || 1;

    const dynamicPrice = basePrice * pricingFactor;
    document.getElementById('dynamic-price').textContent = `$${dynamicPrice.toFixed(2)}`;
}

function addSchedule() {
    const route = document.getElementById('schedule-route').value;
    const flightDate = document.getElementById('flight-date').value;
    const flightTime = document.getElementById('flight-time').value;

    const scheduleList = document.getElementById('schedule-list');
    const listItem = document.createElement('li');
    listItem.textContent = `Route: ${route}, Date: ${flightDate}, Time: ${flightTime}`;
    scheduleList.appendChild(listItem);
}
