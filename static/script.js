async function calculateCost() {
  const response = await fetch('/prices');
  const prices = await response.json();

  const ship = document.getElementById('shipSelect').value;
  let materials = {};

  if (ship === 'windsor') {
    materials = { iron: 120, oak: 40, steel: 10 };
  } else if (ship === 'clipper') {
    materials = { iron: 80, oak: 30, steel: 5 };
  }

  let total = 0;
  for (let mat in materials) {
    if (prices[mat]) {
      total += materials[mat] * prices[mat];
    }
  }

  document.getElementById('result').innerText = `Total cost: ${total.toFixed(2)} doubloons`;
}