// Show unit info panel and image for selected unit
function showUnitInfo(role, unitName) {
  if (!window.units) return;
  const unit = window.units.find(u => u.name === unitName);
  const infoDiv = document.getElementById(role + '-info');
  const imgDiv = document.getElementById(role + '-img');
  const placeholderImg = '/static/img/placeholder.png';
  let imgTag = '';
  if (!unit) {
    infoDiv.innerHTML = '';
    imgDiv.innerHTML = `<img src='${placeholderImg}' alt='No unit selected' width='640' height='750' style='border-radius:12px;opacity:0.5;'>`;
    return;
  }
  if (unit.image_url && typeof unit.image_url === 'string' && unit.image_url.trim() !== '') {
    imgTag = `<img src='${unit.image_url}' alt='${unit.name}' width='640' height='750' style='border-radius:12px;' onerror="this.onerror=null;this.src='${placeholderImg}';">`;
  } else {
    imgTag = `<img src='${placeholderImg}' alt='No unit selected' width='640' height='750' style='border-radius:12px;opacity:0.5;'>`;
  }
  imgDiv.innerHTML = imgTag;
  infoDiv.innerHTML = `
    <div style="border:1px solid #ccc; padding:8px; margin:8px 0;">
      <strong>${unit.name}</strong><br>
      <span>HP: ${unit.hp}, Atk: ${unit.atk}, Spd: ${unit.spd}, Def: ${unit.defense}, Res: ${unit.res}</span><br>
      <span>Movement: ${unit.unit_type}, Weapon: ${unit.weapon_type}</span><br>
      <span>Superboons: ${unit.superboons && unit.superboons.length ? unit.superboons.join(', ') : 'None'}</span><br>
      <span>Superbanes: ${unit.superbanes && unit.superbanes.length ? unit.superbanes.join(', ') : 'None'}</span><br>
      <span>Exclusive Skills: ${unit.exclusive_skills && unit.exclusive_skills.length ? unit.exclusive_skills.join(', ') : 'None'}</span>
    </div>
  `;
}

document.addEventListener('DOMContentLoaded', function() {
  const attackerSelect = document.getElementById('attacker');
  const defenderSelect = document.getElementById('defender');
  if (attackerSelect) showUnitInfo('attacker', attackerSelect.value);
  if (defenderSelect) showUnitInfo('defender', defenderSelect.value);
  if (attackerSelect) attackerSelect.addEventListener('change', function() { showUnitInfo('attacker', this.value); });
  if (defenderSelect) defenderSelect.addEventListener('change', function() { showUnitInfo('defender', this.value); });

  // Auto-submit form on any change
  const form = attackerSelect ? attackerSelect.closest('form') : null;
  if (form) {
    form.querySelectorAll('select').forEach(sel => {
      sel.addEventListener('change', function() {
        form.submit();
      });
    });
  }
});

function addDropdownTooltip(dropdownId, getDetails) {
  const dropdown = document.getElementById(dropdownId);
  if (!dropdown) return;
  let tooltip;
  function showTooltip(e) {
    const selected = dropdown.options[dropdown.selectedIndex];
    const details = getDetails(selected.value);
    if (!details) return;
    if (!tooltip) {
      tooltip = document.createElement('div');
      tooltip.textContent = details;
      Object.assign(tooltip.style, {
        position: 'fixed',
        background: '#33363a',
        color: '#ffe600',
        border: '2px solid #ff003c',
        borderRadius: '8px',
        padding: '8px 14px',
        zIndex: 1000,
        fontSize: '1em',
        pointerEvents: 'none',
      });
      document.body.appendChild(tooltip);
    }
    moveTooltip(e);
  }
  function moveTooltip(e) {
    if (!tooltip) return;
    const { clientX: x, clientY: y } = e;
    tooltip.style.left = `${x + 10}px`;
    tooltip.style.top = `${y + 10}px`;
  }
  dropdown.addEventListener('mouseover', showTooltip);
  dropdown.addEventListener('mousemove', moveTooltip);
  dropdown.addEventListener('mouseout', () => { if (tooltip) tooltip.remove(); tooltip = null; });
}
// Add tooltips to all dropdowns
if (window.weapons && window.skills) {
  addDropdownTooltip('attacker_weapon', (value) => window.weapons.find(w => w.name === value)?.description);
  addDropdownTooltip('defender_weapon', (value) => window.weapons.find(w => w.name === value)?.description);
  addDropdownTooltip('attacker_special', (value) => window.skills.find(s => s.name === value)?.description);
  addDropdownTooltip('defender_special', (value) => window.skills.find(s => s.name === value)?.description);
  addDropdownTooltip('attacker_a', (value) => window.skills.find(s => s.name === value)?.description);
  addDropdownTooltip('defender_a', (value) => window.skills.find(s => s.name === value)?.description);
  addDropdownTooltip('attacker_b', (value) => window.skills.find(s => s.name === value)?.description);
  addDropdownTooltip('defender_b', (value) => window.skills.find(s => s.name === value)?.description);
  addDropdownTooltip('attacker_c', (value) => window.skills.find(s => s.name === value)?.description);
  addDropdownTooltip('defender_c', (value) => window.skills.find(s => s.name === value)?.description);
  addDropdownTooltip('attacker_seal', (value) => window.skills.find(s => s.name === value)?.description);
  addDropdownTooltip('defender_seal', (value) => window.skills.find(s => s.name === value)?.description);
  addDropdownTooltip('attacker_x', (value) => window.skills.find(s => s.name === value)?.description);
  addDropdownTooltip('defender_x', (value) => window.skills.find(s => s.name === value)?.description);
}
