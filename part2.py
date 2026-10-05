TOOLS = [
    {
        "slug": "word-counter",
        "name": "Word Counter",
        "title": "Free Word Counter - Count Words, Characters & Reading Time",
        "desc": "Paste your text to instantly count words, characters, sentences and estimated reading time. Free, private and works offline in your browser.",
        "keywords": "word counter, character counter, count words online, reading time calculator",
        "body": """
      <div class="card">
        <label for="wc-input">Your text</label>
        <textarea id="wc-input" rows="10" placeholder="Paste or type your text here..."></textarea>
        <div class="stats" id="wc-stats">
          <div><span id="wc-words">0</span><small>Words</small></div>
          <div><span id="wc-chars">0</span><small>Characters</small></div>
          <div><span id="wc-sentences">0</span><small>Sentences</small></div>
          <div><span id="wc-minutes">0</span><small>Min read</small></div>
        </div>
      </div>
      <div class="card">
        <button class="btn" onclick="wcClear()">Clear</button>
      </div>
""",
        "script": """
  const input = document.getElementById('wc-input');
  function wcUpdate() {
    const text = input.value;
    const words = text.trim() ? text.trim().split(/\\s+/).length : 0;
    document.getElementById('wc-words').textContent = words;
    document.getElementById('wc-chars').textContent = text.length;
    document.getElementById('wc-sentences').textContent = text.trim() ? (text.match(/[.!?]+/g) || []).length : 0;
    document.getElementById('wc-minutes').textContent = Math.max(1, Math.round(words / 200));
  }
  function wcClear() { input.value = ''; wcUpdate(); }
  input.addEventListener('input', wcUpdate);
  wcUpdate();
""",
    },
    {
        "slug": "case-converter",
        "name": "Case Converter",
        "title": "Free Case Converter - Uppercase, Lowercase & Title Case",
        "desc": "Convert text to UPPERCASE, lowercase, Title Case or Sentence case instantly. A simple, free online text case changer.",
        "keywords": "case converter, uppercase converter, lowercase converter, title case generator",
        "body": """
      <div class="card">
        <textarea id="cc-input" rows="8" placeholder="Type or paste text..."></textarea>
        <div class="row">
          <button class="btn" onclick="ccApply('upper')">UPPERCASE</button>
          <button class="btn" onclick="ccApply('lower')">lowercase</button>
          <button class="btn" onclick="ccApply('title')">Title Case</button>
          <button class="btn" onclick="ccApply('sentence')">Sentence case</button>
          <button class="btn ghost" onclick="ccCopy()">Copy</button>
        </div>
      </div>
""",
        "script": """
  const cc = document.getElementById('cc-input');
  function ccApply(mode) {
    const t = cc.value;
    if (mode === 'upper') cc.value = t.toUpperCase();
    else if (mode === 'lower') cc.value = t.toLowerCase();
    else if (mode === 'title') cc.value = t.replace(/\\w\\S*/g, w => w[0].toUpperCase() + w.slice(1).toLowerCase());
    else cc.value = t.toLowerCase().replace(/(^\\s*\\w|\\.\\s*\\w)/g, m => m.toUpperCase());
  }
  function ccCopy() { cc.select(); document.execCommand('copy'); }
""",
    },
    {
        "slug": "qr-generator",
        "name": "QR Code Generator",
        "title": "Free QR Code Generator - Create QR Codes Instantly",
        "desc": "Generate a QR code for any link or text and download it as an image. Free, no sign-up, works in your browser.",
        "keywords": "qr code generator, free qr code, create qr code online, qr code for link",
        "body": """
      <div class="card">
        <input id="qr-input" type="text" placeholder="https://your-link.com" value="https://example.com">
        <button class="btn" onclick="qrMake()">Generate</button>
        <div id="qr-box" class="qr-box"></div>
      </div>
""",
        "script": """
  function qrMake() {
    const val = document.getElementById('qr-input').value.trim() || 'https://example.com';
    const url = 'https://api.qrserver.com/v1/create-qr-code/?size=240x240&data=' + encodeURIComponent(val);
    document.getElementById('qr-box').innerHTML =
      '<img alt="QR code" src="' + url + '"><p><a href="' + url + '" download="qr.png">Download image</a></p>';
  }
  qrMake();
""",
    },
    {
        "slug": "password-generator",
        "name": "Password Generator",
        "title": "Free Strong Password Generator - Secure Random Passwords",
        "desc": "Create strong, random passwords with custom length and character sets. Generated locally in your browser, nothing is sent to a server.",
        "keywords": "password generator, strong password, random password generator, secure password",
        "body": """
      <div class="card">
        <label for="pg-len">Length: <span id="pg-lenval">16</span></label>
        <input id="pg-len" type="range" min="6" max="48" value="16">
        <div class="row">
          <label><input type="checkbox" id="pg-upper" checked> A-Z</label>
          <label><input type="checkbox" id="pg-lower" checked> a-z</label>
          <label><input type="checkbox" id="pg-num" checked> 0-9</label>
          <label><input type="checkbox" id="pg-sym" checked> !@#</label>
        </div>
        <div class="output" id="pg-out"></div>
        <div class="row">
          <button class="btn" onclick="pgMake()">Generate</button>
          <button class="btn ghost" onclick="pgCopy()">Copy</button>
        </div>
      </div>
""",
        "script": """
  const pgLen = document.getElementById('pg-len');
  pgLen.addEventListener('input', () => { document.getElementById('pg-lenval').textContent = pgLen.value; pgMake(); });
  function pgMake() {
    let chars = '';
    if (document.getElementById('pg-upper').checked) chars += 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
    if (document.getElementById('pg-lower').checked) chars += 'abcdefghijklmnopqrstuvwxyz';
    if (document.getElementById('pg-num').checked) chars += '0123456789';
    if (document.getElementById('pg-sym').checked) chars += '!@#$%^&*()-_=+[]{}';
    if (!chars) chars = 'abcdefghijklmnopqrstuvwxyz';
    const len = +pgLen.value;
    const arr = new Uint32Array(len);
    crypto.getRandomValues(arr);
    let out = '';
    for (let i = 0; i < len; i++) out += chars[arr[i] % chars.length];
    document.getElementById('pg-out').textContent = out;
  }
  function pgCopy() {
    const el = document.getElementById('pg-out');
    navigator.clipboard && navigator.clipboard.writeText(el.textContent);
  }
  pgMake();
""",
    },
    {
        "slug": "lorem-ipsum",
        "name": "Lorem Ipsum Generator",
        "title": "Free Lorem Ipsum Generator - Dummy Placeholder Text",
        "desc": "Generate Lorem Ipsum placeholder text by paragraph, sentence or word count. Ideal for designers and developers.",
        "keywords": "lorem ipsum generator, dummy text, placeholder text generator, filler text",
        "body": """
      <div class="card">
        <div class="row">
          <label>Paragraphs <input id="li-count" type="number" min="1" max="20" value="3"></label>
          <button class="btn" onclick="liMake()">Generate</button>
          <button class="btn ghost" onclick="liCopy()">Copy</button>
        </div>
        <div class="output" id="li-out"></div>
      </div>
""",
        "script": """
  const LI_WORDS = 'lorem ipsum dolor sit amet consectetur adipiscing elit sed do eiusmod tempor incididunt ut labore et dolore magna aliqua enim ad minim veniam quis nostrud exercitation ullamco laboris nisi aliquip ex ea commodo consequat'.split(' ');
  function liMake() {
    const n = Math.min(20, Math.max(1, +document.getElementById('li-count').value || 1));
    let out = '';
    for (let p = 0; p < n; p++) {
      const len = 30 + Math.floor(Math.random() * 30);
      let s = '';
      for (let i = 0; i < len; i++) s += LI_WORDS[Math.floor(Math.random() * LI_WORDS.length)] + ' ';
      out += '<p>' + s.trim().replace(/^./, c => c.toUpperCase()) + '.</p>';
    }
    document.getElementById('li-out').innerHTML = out;
  }
  function liCopy() { navigator.clipboard && navigator.clipboard.writeText(document.getElementById('li-out').innerText); }
  liMake();
""",
    },
    {
        "slug": "age-calculator",
        "name": "Age Calculator",
        "title": "Free Age Calculator - Calculate Your Exact Age in Years, Months & Days",
        "desc": "Find your exact age in years, months and days from your date of birth. Free online age calculator.",
        "keywords": "age calculator, calculate age, how old am i, date of birth calculator",
        "body": """
      <div class="card">
        <label for="age-dob">Date of birth</label>
        <input id="age-dob" type="date">
        <button class="btn" onclick="ageCalc()">Calculate age</button>
        <div class="output" id="age-out"></div>
      </div>
""",
        "script": """
  function ageCalc() {
    const v = document.getElementById('age-dob').value;
    const out = document.getElementById('age-out');
    if (!v) { out.textContent = 'Please choose your date of birth.'; return; }
    const dob = new Date(v + 'T00:00:00');
    const now = new Date();
    if (dob > now) { out.textContent = 'Date of birth cannot be in the future.'; return; }
    let years = now.getFullYear() - dob.getFullYear();
    let months = now.getMonth() - dob.getMonth();
    let days = now.getDate() - dob.getDate();
    if (days < 0) { months--; days += new Date(now.getFullYear(), now.getMonth(), 0).getDate(); }
    if (months < 0) { years--; months += 12; }
    const totalDays = Math.floor((now - dob) / 86400000);
    out.innerHTML = '<strong>' + years + ' years, ' + months + ' months, ' + days + ' days</strong><br>' +
      'About ' + totalDays.toLocaleString() + ' days, or ' + Math.floor(totalDays/7).toLocaleString() + ' weeks.';
  }
""",
    },
    {
        "slug": "percentage-calculator",
        "name": "Percentage Calculator",
        "title": "Free Percentage Calculator - Percent Of, Increase & Decrease",
        "desc": "Calculate percentages online: what is X% of Y, X is what percent of Y, and percentage increase or decrease.",
        "keywords": "percentage calculator, percent of, percentage increase calculator, percentage decrease",
        "body": """
      <div class="card">
        <h3>What is X% of Y?</h3>
        <div class="row">
          <input id="p1a" type="number" placeholder="X" style="max-width:120px">
          <span>% of</span>
          <input id="p1b" type="number" placeholder="Y" style="max-width:120px">
          <button class="btn" onclick="pct1()">=</button>
          <strong id="p1r"></strong>
        </div>
      </div>
      <div class="card">
        <h3>X is what percent of Y?</h3>
        <div class="row">
          <input id="p2a" type="number" placeholder="X" style="max-width:120px">
          <span>is what % of</span>
          <input id="p2b" type="number" placeholder="Y" style="max-width:120px">
          <button class="btn" onclick="pct2()">=</button>
          <strong id="p2r"></strong>
        </div>
      </div>
      <div class="card">
        <h3>Percentage change (from &rarr; to)</h3>
        <div class="row">
          <input id="p3a" type="number" placeholder="from" style="max-width:120px">
          <input id="p3b" type="number" placeholder="to" style="max-width:120px">
          <button class="btn" onclick="pct3()">=</button>
          <strong id="p3r"></strong>
        </div>
      </div>
""",
        "script": """
  const pv = id => parseFloat(document.getElementById(id).value);
  function pct1() { document.getElementById('p1r').textContent = isNaN(pv('p1a'))||isNaN(pv('p1b')) ? '—' : (pv('p1a')/100*pv('p1b')).toLocaleString(); }
  function pct2() { document.getElementById('p2r').textContent = isNaN(pv('p2a'))||!pv('p2b') ? '—' : (pv('p2a')/pv('p2b')*100).toFixed(2) + '%'; }
  function pct3() { const a=pv('p3a'), b=pv('p3b'); document.getElementById('p3r').textContent = isNaN(a)||!a ? '—' : (((b-a)/Math.abs(a))*100).toFixed(2) + '%'; }
""",
    },
    {
        "slug": "bmi-calculator",
        "name": "BMI Calculator",
        "title": "Free BMI Calculator - Body Mass Index for Adults",
        "desc": "Calculate your Body Mass Index from height and weight and see your category. Free online BMI calculator.",
        "keywords": "bmi calculator, body mass index, bmi chart, healthy weight calculator",
        "body": """
      <div class="card">
        <div class="row">
          <label>Height (cm) <input id="bmi-h" type="number" value="170" style="max-width:120px"></label>
          <label>Weight (kg) <input id="bmi-w" type="number" value="70" style="max-width:120px"></label>
        </div>
        <button class="btn" onclick="bmiCalc()">Calculate BMI</button>
        <div class="output" id="bmi-out"></div>
      </div>
""",
        "script": """
  function bmiCalc() {
    const h = parseFloat(document.getElementById('bmi-h').value) / 100;
    const w = parseFloat(document.getElementById('bmi-w').value);
    const out = document.getElementById('bmi-out');
    if (!h || !w || h <= 0 || w <= 0) { out.textContent = 'Enter a valid height and weight.'; return; }
    const bmi = w / (h * h);
    let cat = 'Normal weight';
    if (bmi < 18.5) cat = 'Underweight';
    else if (bmi >= 25 && bmi < 30) cat = 'Overweight';
    else if (bmi >= 30) cat = 'Obese';
    out.innerHTML = '<strong>BMI: ' + bmi.toFixed(1) + '</strong> — ' + cat;
  }
""",
    },
    {
        "slug": "unit-converter",
        "name": "Unit Converter",
        "title": "Free Unit Converter - Length, Weight & Temperature",
        "desc": "Convert between common units of length, weight and temperature instantly. Free online unit converter.",
        "keywords": "unit converter, length converter, weight converter, temperature converter, cm to inches",
        "body": """
      <div class="card">
        <div class="row">
          <select id="uc-cat" onchange="ucFill()">
            <option value="length">Length</option>
            <option value="weight">Weight</option>
            <option value="temp">Temperature</option>
          </select>
          <input id="uc-val" type="number" value="1" style="max-width:120px">
          <select id="uc-from"></select>
          <span>to</span>
          <select id="uc-to"></select>
          <button class="btn" onclick="ucConvert()">Convert</button>
        </div>
        <div class="output" id="uc-out"></div>
      </div>
""",
        "script": """
  const UC = {
    length: { m:1, km:1000, cm:0.01, mm:0.001, inch:0.0254, ft:0.3048, yd:0.9144, mile:1609.344 },
    weight: { kg:1, g:0.001, mg:0.000001, lb:0.45359237, oz:0.028349523125, ton:1000 }
  };
  function ucFill() {
    const cat = document.getElementById('uc-cat').value;
    const from = document.getElementById('uc-from'), to = document.getElementById('uc-to');
    from.innerHTML = ''; to.innerHTML = '';
    const units = cat === 'temp' ? ['C','F','K'] : Object.keys(UC[cat]);
    units.forEach(u => { from.add(new Option(u,u)); to.add(new Option(u,u)); });
    if (units.length > 1) to.value = units[1];
    ucConvert();
  }
  function ucConvert() {
    const cat = document.getElementById('uc-cat').value;
    const v = parseFloat(document.getElementById('uc-val').value);
    const f = document.getElementById('uc-from').value, t = document.getElementById('uc-to').value;
    const out = document.getElementById('uc-out');
    if (isNaN(v)) { out.textContent = 'Enter a number.'; return; }
    let res;
    if (cat === 'temp') {
      const c = f === 'C' ? v : f === 'F' ? (v - 32) * 5/9 : v - 273.15;
      res = t === 'C' ? c : t === 'F' ? c * 9/5 + 32 : c + 273.15;
    } else {
      res = v * UC[cat][f] / UC[cat][t];
    }
    out.innerHTML = '<strong>' + v + ' ' + f + ' = ' + (+res.toFixed(6)) + ' ' + t + '</strong>';
  }
  ucFill();
""",
    },
    {
        "slug": "image-compressor",
        "name": "Image Compressor",
        "title": "Free Image Compressor - Compress JPG & PNG Online",
        "desc": "Compress JPG and PNG images in your browser without uploading them. Adjust quality and download the smaller file.",
        "keywords": "image compressor, compress jpg, compress png, reduce image size online",
        "body": """
      <div class="card">
        <input id="ic-file" type="file" accept="image/*">
        <label for="ic-q">Quality: <span id="ic-qv">70</span>%</label>
        <input id="ic-q" type="range" min="10" max="100" value="70">
        <button class="btn" onclick="icCompress()">Compress</button>
        <div class="output" id="ic-out"></div>
      </div>
""",
        "script": """
  const icQ = document.getElementById('ic-q');
  icQ.addEventListener('input', () => document.getElementById('ic-qv').textContent = icQ.value);
  function icCompress() {
    const file = document.getElementById('ic-file').files[0];
    const out = document.getElementById('ic-out');
    if (!file) { out.textContent = 'Choose an image first.'; return; }
    const img = new Image();
    img.onload = () => {
      const c = document.createElement('canvas');
      c.width = img.width; c.height = img.height;
      c.getContext('2d').drawImage(img, 0, 0);
      c.toBlob(blob => {
        const url = URL.createObjectURL(blob);
        const saved = Math.max(0, Math.round((1 - blob.size / file.size) * 100));
        out.innerHTML = 'Original: ' + Math.round(file.size/1024) + ' KB → Compressed: ' +
          Math.round(blob.size/1024) + ' KB (' + saved + '% smaller)<br>' +
          '<a href="' + url + '" download="compressed.jpg">Download compressed image</a>';
      }, 'image/jpeg', icQ.value / 100);
    };
    img.onerror = () => out.textContent = 'Could not read that image.';
    img.src = URL.createObjectURL(file);
  }
""",
    },
    {
        "slug": "json-formatter",
        "name": "JSON Formatter",
        "title": "Free JSON Formatter & Validator - Beautify JSON Online",
        "desc": "Format, beautify and validate JSON instantly in your browser. Spot syntax errors with a clear message.",
        "keywords": "json formatter, json validator, beautify json, json beautifier online",
        "body": """
      <div class="card">
        <label for="jf-in">JSON input</label>
        <textarea id="jf-in" rows="8" placeholder='{"hello":"world"}'></textarea>
        <div class="row">
          <button class="btn" onclick="jfFormat(2)">Format</button>
          <button class="btn" onclick="jfFormat(0)">Minify</button>
          <button class="btn ghost" onclick="jfClear()">Clear</button>
        </div>
        <div class="output" id="jf-out"></div>
      </div>
""",
        "script": """
  function jfFormat(space) {
    const out = document.getElementById('jf-out');
    try {
      const obj = JSON.parse(document.getElementById('jf-in').value);
      out.textContent = JSON.stringify(obj, null, space);
      out.style.color = '';
    } catch (e) { out.textContent = 'Invalid JSON: ' + e.message; out.style.color = '#f87171'; }
  }
  function jfClear() { document.getElementById('jf-in').value = ''; document.getElementById('jf-out').textContent = ''; }
""",
    },
    {
        "slug": "base64-encoder",
        "name": "Base64 Encoder",
        "title": "Free Base64 Encoder & Decoder - Encode Text Online",
        "desc": "Encode text to Base64 or decode Base64 back to text. Handles Unicode safely, all in your browser.",
        "keywords": "base64 encoder, base64 decoder, encode base64, decode base64 online",
        "body": """
      <div class="card">
        <label for="b64-in">Text or Base64</label>
        <textarea id="b64-in" rows="6"></textarea>
        <div class="row">
          <button class="btn" onclick="b64Do('enc')">Encode to Base64</button>
          <button class="btn" onclick="b64Do('dec')">Decode from Base64</button>
        </div>
        <div class="output" id="b64-out"></div>
      </div>
""",
        "script": """
  function b64Do(mode) {
    const out = document.getElementById('b64-out');
    const v = document.getElementById('b64-in').value;
    try {
      if (mode === 'enc') out.textContent = btoa(unescape(encodeURIComponent(v)));
      else out.textContent = decodeURIComponent(escape(atob(v.trim())));
    } catch (e) { out.textContent = 'Error: input is not valid for this operation.'; }
  }
""",
    },
    {
        "slug": "random-number-generator",
        "name": "Random Number Generator",
        "title": "Free Random Number Generator - Pick Numbers in a Range",
        "desc": "Generate random numbers within a range, with or without duplicates. Great for draws and giveaways.",
        "keywords": "random number generator, random number picker, rng, lottery number generator",
        "body": """
      <div class="card">
        <div class="row">
          <label>Min <input id="rn-min" type="number" value="1" style="max-width:100px"></label>
          <label>Max <input id="rn-max" type="number" value="100" style="max-width:100px"></label>
          <label>How many <input id="rn-count" type="number" value="1" style="max-width:100px"></label>
          <label><input type="checkbox" id="rn-uniq" checked> Unique</label>
        </div>
        <button class="btn" onclick="rnGen()">Generate</button>
        <div class="output" id="rn-out"></div>
      </div>
""",
        "script": """
  function rnGen() {
    const min = Math.ceil(+document.getElementById('rn-min').value);
    const max = Math.floor(+document.getElementById('rn-max').value);
    const count = Math.max(1, Math.min(1000, +document.getElementById('rn-count').value || 1));
    const uniq = document.getElementById('rn-uniq').checked;
    const out = document.getElementById('rn-out');
    if (max < min) { out.textContent = 'Max must be greater than min.'; return; }
    const range = max - min + 1;
    if (uniq && count > range) { out.textContent = 'Cannot pick ' + count + ' unique numbers from a range of ' + range + '.'; return; }
    const res = [];
    if (uniq) {
      const pool = Array.from({length: range}, (_, i) => min + i);
      for (let i = 0; i < count; i++) res.push(pool.splice(Math.floor(Math.random()*pool.length), 1)[0]);
    } else {
      for (let i = 0; i < count; i++) res.push(min + Math.floor(Math.random()*range));
    }
    out.textContent = res.join(', ');
  }
  rnGen();
""",
    },
    {
        "slug": "unix-timestamp",
        "name": "Unix Timestamp Converter",
        "title": "Unix Timestamp Converter - Epoch to Date and Back",
        "desc": "Convert a Unix timestamp to a human-readable date, or a date to a Unix timestamp. Shows the live current epoch time.",
        "keywords": "unix timestamp converter, epoch converter, timestamp to date, epoch time now",
        "body": """
      <div class="card">
        <h3>Current Unix time</h3>
        <div class="output"><strong id="ts-now"></strong></div>
      </div>
      <div class="card">
        <h3>Timestamp &rarr; Date</h3>
        <div class="row">
          <input id="ts-in" type="number" placeholder="e.g. 1700000000" style="max-width:220px">
          <button class="btn" onclick="tsToDate()">Convert</button>
          <strong id="ts-dater"></strong>
        </div>
      </div>
      <div class="card">
        <h3>Date &rarr; Timestamp</h3>
        <div class="row">
          <input id="ts-date" type="datetime-local">
          <button class="btn" onclick="dateToTs()">Convert</button>
          <strong id="ts-tsr"></strong>
        </div>
      </div>
""",
        "script": """
  function tsTick() { document.getElementById('ts-now').textContent = Math.floor(Date.now()/1000); }
  setInterval(tsTick, 1000); tsTick();
  function tsToDate() {
    const v = +document.getElementById('ts-in').value;
    document.getElementById('ts-dater').textContent = v ? new Date(v*1000).toString() : '—';
  }
  function dateToTs() {
    const v = document.getElementById('ts-date').value;
    document.getElementById('ts-tsr').textContent = v ? Math.floor(new Date(v).getTime()/1000) : '—';
  }
""",
    },
    {
        "slug": "color-converter",
        "name": "Color Converter",
        "title": "Free Color Converter - HEX, RGB and HSL",
        "desc": "Convert colors between HEX, RGB and HSL and preview the colour. Free online colour converter for designers and developers.",
        "keywords": "hex to rgb, rgb to hex, color converter, hsl converter, color picker",
        "body": """
      <div class="card">
        <div class="row">
          <input id="col-in" type="text" value="#38bdf8" style="max-width:160px">
          <input id="col-pick" type="color" value="#38bdf8">
          <button class="btn" onclick="colConvert()">Convert</button>
        </div>
        <div class="row"><div id="col-swatch" style="width:100%;height:60px;border-radius:8px;background:#38bdf8"></div></div>
        <div class="output" id="col-out"></div>
      </div>
""",
        "script": """
  const colIn = document.getElementById('col-in'), colPick = document.getElementById('col-pick');
  colPick.addEventListener('input', () => { colIn.value = colPick.value; colConvert(); });
  function colConvert() {
    let hex = colIn.value.trim().replace('#','');
    if (hex.length === 3) hex = hex.split('').map(c => c+c).join('');
    if (!/^[0-9a-fA-F]{6}$/.test(hex)) { document.getElementById('col-out').textContent = 'Enter a valid HEX colour, e.g. #38bdf8.'; return; }
    const r = parseInt(hex.slice(0,2),16), g = parseInt(hex.slice(2,4),16), b = parseInt(hex.slice(4,6),16);
    const rr = r/255, gg = g/255, bb = b/255;
    const max = Math.max(rr,gg,bb), min = Math.min(rr,gg,bb);
    let h = 0, s = 0;
    const l = (max+min)/2;
    if (max !== min) {
      const d = max-min;
      s = l > 0.5 ? d/(2-max-min) : d/(max+min);
      h = max === rr ? (gg-bb)/d + (gg<bb?6:0) : max === gg ? (bb-rr)/d + 2 : (rr-gg)/d + 4;
      h *= 60;
    }
    document.getElementById('col-swatch').style.background = '#'+hex;
    colPick.value = '#'+hex;
    document.getElementById('col-out').innerHTML =
      '<strong>HEX</strong> #' + hex.toLowerCase() + '<br>' +
      '<strong>RGB</strong> rgb(' + r + ', ' + g + ', ' + b + ')<br>' +
      '<strong>HSL</strong> hsl(' + Math.round(h) + ', ' + Math.round(s*100) + '%, ' + Math.round(l*100) + '%)';
  }
  colConvert();
""",
    },
    {
        "slug": "image-resizer",
        "name": "Image Resizer",
        "title": "Free Image Resizer - Resize Photos Online in Your Browser",
        "desc": "Resize images to any width and height online. Keep the aspect ratio and download instantly, without uploading your photos.",
        "keywords": "image resizer, resize image online, resize photo, change image size",
        "body": """
      <div class="card">
        <input id="ir-file" type="file" accept="image/*">
        <div class="row">
          <label>Width <input id="ir-w" type="number" placeholder="px" style="max-width:120px"></label>
          <label>Height <input id="ir-h" type="number" placeholder="px" style="max-width:120px"></label>
          <label><input type="checkbox" id="ir-ratio" checked> Keep ratio</label>
        </div>
        <button class="btn" onclick="irResize()">Resize</button>
        <div class="output" id="ir-out"></div>
      </div>
""",
        "script": """
  const irFile = document.getElementById('ir-file');
  let irImg = null;
  irFile.addEventListener('change', () => {
    const f = irFile.files[0]; if (!f) return;
    irImg = new Image();
    irImg.onload = () => {
      document.getElementById('ir-w').value = irImg.width;
      document.getElementById('ir-h').value = irImg.height;
      document.getElementById('ir-out').textContent = 'Loaded ' + irImg.width + 'x' + irImg.height + ' image.';
    };
    irImg.src = URL.createObjectURL(f);
  });
  document.getElementById('ir-w').addEventListener('input', () => {
    if (irImg && document.getElementById('ir-ratio').checked) {
      document.getElementById('ir-h').value = Math.round(document.getElementById('ir-w').value * irImg.height / irImg.width);
    }
  });
  function irResize() {
    const out = document.getElementById('ir-out');
    if (!irImg) { out.textContent = 'Choose an image first.'; return; }
    const w = Math.max(1, +document.getElementById('ir-w').value || irImg.width);
    const h = Math.max(1, +document.getElementById('ir-h').value || irImg.height);
    const c = document.createElement('canvas'); c.width = w; c.height = h;
    c.getContext('2d').drawImage(irImg, 0, 0, w, h);
    c.toBlob(blob => {
      out.innerHTML = 'Resized to ' + w + 'x' + h + ' (' + Math.round(blob.size/1024) + ' KB)<br>' +
        '<a href="' + URL.createObjectURL(blob) + '" download="resized.png">Download resized image</a>';
    }, 'image/png');
  }
""",
    },
    {
        "slug": "pomodoro-timer",
        "name": "Pomodoro Timer",
        "title": "Free Pomodoro Timer - 25 Minute Focus Timer Online",
        "desc": "A simple Pomodoro timer with 25 minute work and 5 minute break sessions. Stay focused and track your productivity.",
        "keywords": "pomodoro timer, focus timer, 25 minute timer, study timer online",
        "body": """
      <div class="card" style="text-align:center">
        <div class="output" id="pomo-display" style="font-size:3rem;font-weight:700">25:00</div>
        <div class="row" style="justify-content:center">
          <button class="btn" id="pomo-start" onclick="pomoToggle()">Start</button>
          <button class="btn ghost" onclick="pomoReset()">Reset</button>
          <button class="btn ghost" onclick="pomoMode('work')">Work 25m</button>
          <button class="btn ghost" onclick="pomoMode('break')">Break 5m</button>
        </div>
        <p id="pomo-label" style="color:var(--muted)">Focus session</p>
      </div>
""",
        "script": """
  let pomoLeft = 25 * 60, pomoRunning = false, pomoTimer = null, pomoName = 'Focus session';
  function pomoRender() {
    const m = Math.floor(pomoLeft/60), s = pomoLeft % 60;
    document.getElementById('pomo-display').textContent = (m<10?'0':'')+m+':'+(s<10?'0':'')+s;
  }
  function pomoToggle() {
    pomoRunning = !pomoRunning;
    document.getElementById('pomo-start').textContent = pomoRunning ? 'Pause' : 'Start';
    if (pomoRunning) {
      pomoTimer = setInterval(() => {
        if (pomoLeft > 0) { pomoLeft--; pomoRender(); }
        else { clearInterval(pomoTimer); pomoRunning = false;
          document.getElementById('pomo-start').textContent = 'Start';
          try { new AudioContext(); } catch(e) {}
        }
      }, 1000);
    } else { clearInterval(pomoTimer); }
  }
  function pomoReset() { clearInterval(pomoTimer); pomoRunning = false; document.getElementById('pomo-start').textContent='Start'; pomoMode(pomoName==='Break time'?'break':'work'); }
  function pomoMode(mode) {
    clearInterval(pomoTimer); pomoRunning = false; document.getElementById('pomo-start').textContent='Start';
    pomoName = mode === 'work' ? 'Focus session' : 'Break time';
    pomoLeft = (mode === 'work' ? 25 : 5) * 60;
    document.getElementById('pomo-label').textContent = pomoName;
    pomoRender();
  }
  pomoRender();
""",
    },
    {
        "slug": "hash-generator",
        "name": "Hash Generator",
        "title": "Free SHA-256 & MD5 Hash Generator Online",
        "desc": "Generate SHA-256, SHA-1 and SHA-512 hashes of any text, plus a non-cryptographic MD5-style checksum. Runs in your browser.",
        "keywords": "sha256 generator, md5 generator, hash generator, sha512 online",
        "body": """
      <div class="card">
        <label for="hash-in">Text to hash</label>
        <textarea id="hash-in" rows="4" placeholder="Type text..."></textarea>
        <button class="btn" onclick="hashRun()">Generate hashes</button>
        <div class="output" id="hash-out"></div>
      </div>
""",
        "script": """
  async function hashRun() {
    const out = document.getElementById('hash-out');
    const data = new TextEncoder().encode(document.getElementById('hash-in').value);
    const algs = ['SHA-1','SHA-256','SHA-512'];
    let res = '';
    for (const alg of algs) {
      const buf = await crypto.subtle.digest(alg, data);
      res += '<strong>' + alg + '</strong>: ' + Array.from(new Uint8Array(buf)).map(b=>b.toString(16).padStart(2,'0')).join('') + '<br>';
    }
    out.innerHTML = res;
  }
""",
    },
    {
        "slug": "url-encoder",
        "name": "URL Encoder / Decoder",
        "title": "Free URL Encoder & Decoder - Percent-Encoding Online",
        "desc": "Encode text for use in URLs (percent-encoding) or decode an encoded URL back to readable text. Free and instant.",
        "keywords": "url encoder, url decoder, percent encoding, encode url online",
        "body": """
      <div class="card">
        <label for="url-in">Text or encoded URL</label>
        <textarea id="url-in" rows="5"></textarea>
        <div class="row">
          <button class="btn" onclick="urlDo('enc')">Encode</button>
          <button class="btn" onclick="urlDo('dec')">Decode</button>
        </div>
        <div class="output" id="url-out"></div>
      </div>
""",
        "script": """
  function urlDo(mode) {
    const out = document.getElementById('url-out');
    try {
      out.textContent = mode === 'enc'
        ? encodeURIComponent(document.getElementById('url-in').value)
        : decodeURIComponent(document.getElementById('url-in').value);
    } catch (e) { out.textContent = 'Error: input is not valid for decoding.'; }
  }
""",
    },
    {
        "slug": "roman-numeral-converter",
        "name": "Roman Numeral Converter",
        "title": "Free Roman Numeral Converter - Numbers to Roman Numerals",
        "desc": "Convert numbers to Roman numerals and Roman numerals back to numbers. Supports 1 to 3999.",
        "keywords": "roman numeral converter, numbers to roman numerals, roman numerals to numbers",
        "body": """
      <div class="card">
        <div class="row">
          <input id="rn2-input" type="text" placeholder="e.g. 1987 or MCMLXXXVII" style="max-width:260px">
          <button class="btn" onclick="romanConvert()">Convert</button>
        </div>
        <div class="output" id="rn2-out"></div>
      </div>
""",
        "script": """
  const ROMAN = [[1000,'M'],[900,'CM'],[500,'D'],[400,'CD'],[100,'C'],[90,'XC'],[50,'L'],[40,'XL'],[10,'X'],[9,'IX'],[5,'V'],[4,'IV'],[1,'I']];
  function romanConvert() {
    const v = document.getElementById('rn2-input').value.trim().toUpperCase();
    const out = document.getElementById('rn2-out');
    if (/^[0-9]+$/.test(v)) {
      let n = +v;
      if (n < 1 || n > 3999) { out.textContent = 'Please enter a number from 1 to 3999.'; return; }
      let r = '';
      for (const [val, sym] of ROMAN) while (n >= val) { r += sym; n -= val; }
      out.innerHTML = '<strong>' + v + ' = ' + r + '</strong>';
    } else if (/^[MDCLXVI]+$/.test(v)) {
      let n = 0;
      for (let i = 0; i < v.length; i++) {
        const cur = ROMAN.find(x => x[1] === v[i])[0];
        const nxt = ROMAN.find(x => x[1] === v[i+1]);
        n += (nxt && cur < nxt[0]) ? -cur : cur;
      }
      out.innerHTML = '<strong>' + v + ' = ' + n + '</strong>';
    } else { out.textContent = 'Enter a number (1-3999) or a Roman numeral.'; }
  }
""",
    },
    {
        "slug": "tip-calculator",
        "name": "Tip Calculator",
        "title": "Free Tip Calculator - Split a Bill and Calculate Tips",
        "desc": "Calculate the tip and split a restaurant bill between any number of people. Free online tip calculator.",
        "keywords": "tip calculator, bill splitter, calculate tip, restaurant tip calculator",
        "body": """
      <div class="card">
        <div class="row">
          <label>Bill <input id="tip-bill" type="number" value="50" style="max-width:120px"></label>
          <label>Tip % <input id="tip-pct" type="number" value="15" style="max-width:100px"></label>
          <label>People <input id="tip-people" type="number" value="2" min="1" style="max-width:100px"></label>
          <button class="btn" onclick="tipCalc()">Calculate</button>
        </div>
        <div class="output" id="tip-out"></div>
      </div>
""",
        "script": """
  function tipCalc() {
    const bill = +document.getElementById('tip-bill').value || 0;
    const pct = +document.getElementById('tip-pct').value || 0;
    const people = Math.max(1, +document.getElementById('tip-people').value || 1);
    const tip = bill * pct / 100;
    const total = bill + tip;
    document.getElementById('tip-out').innerHTML =
      '<strong>Tip: ' + tip.toFixed(2) + '</strong><br>' +
      'Total: ' + total.toFixed(2) + '<br>' +
      'Each person pays: ' + (total / people).toFixed(2);
  }
  tipCalc();
""",
    },
    {
        "slug": "date-difference",
        "name": "Date Difference Calculator",
        "title": "Free Date Difference Calculator - Days Between Two Dates",
        "desc": "Calculate the number of days, weeks and months between two dates. Free online date difference calculator.",
        "keywords": "date difference calculator, days between dates, date calculator, how many days until",
        "body": """
      <div class="card">
        <div class="row">
          <label>From <input id="dd-from" type="date"></label>
          <label>To <input id="dd-to" type="date"></label>
          <button class="btn" onclick="ddCalc()">Calculate</button>
        </div>
        <div class="output" id="dd-out"></div>
      </div>
""",
        "script": """
  function ddCalc() {
    const f = document.getElementById('dd-from').value, t = document.getElementById('dd-to').value;
    const out = document.getElementById('dd-out');
    if (!f || !t) { out.textContent = 'Pick both dates.'; return; }
    const a = new Date(f+'T00:00:00'), b = new Date(t+'T00:00:00');
    const days = Math.round((b - a) / 86400000);
    out.innerHTML = '<strong>' + Math.abs(days) + ' days</strong><br>' +
      Math.abs(days/7).toFixed(1) + ' weeks, about ' + Math.abs(days/30.44).toFixed(1) + ' months.<br>' +
      (days < 0 ? '(the second date is earlier)' : '');
  }
""",
    },
    {
        "slug": "loan-emi-calculator",
        "name": "Loan EMI Calculator",
        "title": "Free Loan EMI Calculator - Monthly Payment & Total Interest",
        "desc": "Calculate the monthly EMI, total interest and total payment for a loan. Free online EMI calculator.",
        "keywords": "emi calculator, loan calculator, monthly payment calculator, mortgage calculator",
        "body": """
      <div class="card">
        <div class="row">
          <label>Loan amount <input id="emi-p" type="number" value="100000" style="max-width:150px"></label>
          <label>Annual interest % <input id="emi-r" type="number" value="10" style="max-width:120px"></label>
          <label>Years <input id="emi-y" type="number" value="5" style="max-width:100px"></label>
          <button class="btn" onclick="emiCalc()">Calculate</button>
        </div>
        <div class="output" id="emi-out"></div>
      </div>
""",
        "script": """
  function emiCalc() {
    const P = +document.getElementById('emi-p').value || 0;
    const annual = +document.getElementById('emi-r').value || 0;
    const years = +document.getElementById('emi-y').value || 1;
    const r = annual / 12 / 100, n = years * 12;
    const emi = r === 0 ? P / n : P * r * Math.pow(1 + r, n) / (Math.pow(1 + r, n) - 1);
    const total = emi * n;
    document.getElementById('emi-out').innerHTML =
      '<strong>Monthly EMI: ' + emi.toFixed(2) + '</strong><br>' +
      'Total interest: ' + (total - P).toFixed(2) + '<br>' +
      'Total payment: ' + total.toFixed(2);
  }
  emiCalc();
""",
    },
    {
        "slug": "word-to-pdf-notes",
        "name": "Text to PDF",
        "title": "Free Text to PDF Converter - Turn Notes into a PDF",
        "desc": "Paste or type text and download it as a clean PDF file. Free online text to PDF converter, works in your browser.",
        "keywords": "text to pdf, notes to pdf, convert text to pdf online, plain text to pdf",
        "body": """
      <div class="card">
        <label for="t2p-in">Your text</label>
        <textarea id="t2p-in" rows="10" placeholder="Type or paste your notes here..."></textarea>
        <button class="btn" onclick="t2pMake()">Create PDF</button>
        <div class="output" id="t2p-out"></div>
      </div>
""",
        "script": """
  function t2pEscape(s) { return s.replace(/\\\\/g,'\\\\\\\\').replace(/\\(/g,'\\\\(').replace(/\\)/g,'\\\\)'); }
  function t2pMake() {
    const text = document.getElementById('t2p-in').value;
    const out = document.getElementById('t2p-out');
    if (!text.trim()) { out.textContent = 'Enter some text first.'; return; }
    const lines = text.replace(/\\r/g,'').split('\\n').slice(0, 48);
    let content = 'BT /F1 12 Tf 50 760 Td 16 TL\\n';
    for (const line of lines) content += '(' + t2pEscape(line.slice(0, 90)) + ') Tj T*\\n';
    content += 'ET';
    const objects = [
      '<< /Type /Catalog /Pages 2 0 R >>',
      '<< /Type /Pages /Kids [3 0 R] /Count 1 >>',
      '<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>',
      '<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>',
      '<< /Length ' + content.length + ' >>\\nstream\\n' + content + '\\nendstream'
    ];
    let pdf = '%PDF-1.4\\n';
    const offsets = [0];
    objects.forEach((obj, i) => { offsets.push(pdf.length); pdf += (i+1) + ' 0 obj\\n' + obj + '\\nendobj\\n'; });
    const xref = pdf.length;
    pdf += 'xref\\n0 ' + (objects.length+1) + '\\n0000000000 65535 f \\n';
    for (let i = 1; i <= objects.length; i++) pdf += String(offsets[i]).padStart(10,'0') + ' 00000 n \\n';
    pdf += 'trailer\\n<< /Size ' + (objects.length+1) + ' /Root 1 0 R >>\\nstartxref\\n' + xref + '\\n%%EOF';
    const blob = new Blob([pdf], {type:'application/pdf'});
    out.innerHTML = 'PDF created (' + Math.round(blob.size/1024) + ' KB)<br><a href="' + URL.createObjectURL(blob) + '" download="notes.pdf">Download PDF</a>';
  }
""",
    },
    {
        "slug": "text-repeater",
        "name": "Text Repeater",
        "title": "Free Text Repeater - Repeat Any Text Online",
        "desc": "Repeat a word, sentence or line as many times as you need, with an optional separator. Runs entirely in your browser.",
        "keywords": "text repeater, repeat text online, word repeater, repeat sentence multiple times",
        "body": """
      <div class="card">
        <label for="tr-in">Text to repeat</label>
        <textarea id="tr-in" rows="4" placeholder="Type text here..."></textarea>
        <label for="tr-n">Times: <span id="tr-nv">10</span></label>
        <input id="tr-n" type="range" min="1" max="500" value="10">
        <label for="tr-sep">Separator</label>
        <select id="tr-sep">
          <option value="newline">New line</option>
          <option value="space">Space</option>
          <option value="none">None</option>
        </select>
        <button class="btn" onclick="trRun()">Repeat</button>
        <div class="output" id="tr-out"></div>
      </div>
""",
        "script": """
  const trN = document.getElementById('tr-n');
  trN.addEventListener('input', () => document.getElementById('tr-nv').textContent = trN.value);
  function trRun() {
    const text = document.getElementById('tr-in').value;
    const n = parseInt(trN.value, 10);
    const mode = document.getElementById('tr-sep').value;
    const sep = mode === 'newline' ? '\\n' : (mode === 'space' ? ' ' : '');
    const out = document.getElementById('tr-out');
    if (!text) { out.textContent = 'Enter some text first.'; return; }
    const result = Array(n).fill(text).join(sep);
    out.innerHTML = '<textarea rows="8" id="tr-res"></textarea><br><button class="btn" onclick="trCopy()">Copy</button>';
    document.getElementById('tr-res').value = result;
  }
  function trCopy() {
    const el = document.getElementById('tr-res');
    el.select();
    document.execCommand('copy');
  }
""",
    },
    {
        "slug": "remove-duplicate-lines",
        "name": "Remove Duplicate Lines",
        "title": "Remove Duplicate Lines Online - Free Duplicate Line Remover",
        "desc": "Paste a list and remove repeated lines instantly. Ignore case or leading spaces if you want.",
        "keywords": "remove duplicate lines, delete repeated lines, dedupe list online, unique lines",
        "body": """
      <div class="card">
        <label for="rd-in">Your list</label>
        <textarea id="rd-in" rows="8" placeholder="One item per line..."></textarea>
        <label><input type="checkbox" id="rd-case"> Ignore case</label>
        <label><input type="checkbox" id="rd-trim"> Ignore leading/trailing spaces</label>
        <button class="btn" onclick="rdRun()">Remove duplicates</button>
        <div class="output" id="rd-out"></div>
      </div>
""",
        "script": """
  function rdRun() {
    const lines = document.getElementById('rd-in').value.split('\\n');
    const ic = document.getElementById('rd-case').checked;
    const it = document.getElementById('rd-trim').checked;
    const seen = new Set();
    const outLines = [];
    let removed = 0;
    for (let line of lines) {
      let key = line;
      if (it) { key = key.trim(); if (key === '') continue; }
      if (ic) key = key.toLowerCase();
      if (seen.has(key)) { removed++; continue; }
      seen.add(key);
      outLines.push(line);
    }
    const out = document.getElementById('rd-out');
    out.innerHTML = '<textarea rows="8" id="rd-res"></textarea><br>' +
      '<span class="muted">Removed ' + removed + ' duplicate line(s). ' + outLines.length + ' remain.</span>';
    document.getElementById('rd-res').value = outLines.join('\\n');
  }
""",
    },
    {
        "slug": "sort-lines",
        "name": "Sort Lines",
        "title": "Sort Lines Alphabetically Online - Free Line Sorter",
        "desc": "Sort lines alphabetically or numerically, ascending or descending. Remove duplicates and blank lines at the same time.",
        "keywords": "sort lines alphabetically, line sorter, sort text online, alphabetical order sorter",
        "body": """
      <div class="card">
        <label for="sl-in">Your list</label>
        <textarea id="sl-in" rows="8" placeholder="One item per line..."></textarea>
        <label for="sl-mode">Sort</label>
        <select id="sl-mode">
          <option value="az">A to Z</option>
          <option value="za">Z to A</option>
          <option value="num">Numeric (smallest first)</option>
          <option value="len">By length (shortest first)</option>
        </select>
        <label><input type="checkbox" id="sl-unique"> Remove duplicates</label>
        <button class="btn" onclick="slRun()">Sort</button>
        <div class="output" id="sl-out"></div>
      </div>
""",
        "script": """
  function slRun() {
    let lines = document.getElementById('sl-in').value.split('\\n').filter(l => l.trim() !== '');
    const mode = document.getElementById('sl-mode').value;
    if (document.getElementById('sl-unique').checked) lines = Array.from(new Set(lines));
    if (mode === 'az') lines.sort((a,b) => a.localeCompare(b));
    else if (mode === 'za') lines.sort((a,b) => b.localeCompare(a));
    else if (mode === 'num') lines.sort((a,b) => parseFloat(a) - parseFloat(b));
    else lines.sort((a,b) => a.length - b.length);
    const out = document.getElementById('sl-out');
    out.innerHTML = '<textarea rows="8" id="sl-res"></textarea>';
    document.getElementById('sl-res').value = lines.join('\\n');
  }
""",
    },
    {
        "slug": "word-frequency-counter",
        "name": "Word Frequency Counter",
        "title": "Word Frequency Counter - Find Most Common Words Online",
        "desc": "See which words appear most often in your text, ranked by count. Useful for SEO, essays and editing.",
        "keywords": "word frequency counter, most common words, word count analysis, keyword density checker",
        "body": """
      <div class="card">
        <label for="wf-in">Your text</label>
        <textarea id="wf-in" rows="8" placeholder="Paste text here..."></textarea>
        <label><input type="checkbox" id="wf-stop"> Ignore common words (the, and, of...)</label>
        <button class="btn" onclick="wfRun()">Count words</button>
        <div class="output" id="wf-out"></div>
      </div>
""",
        "script": """
  const WF_STOP = new Set('the a an and or but if in on at to of for with is are was were be been it its this that these those as by from you your we our they their he she his her i me my not no do does did can will would could should'.split(' '));
  function wfRun() {
    const text = document.getElementById('wf-in').value.toLowerCase();
    const stop = document.getElementById('wf-stop').checked;
    const words = text.match(/[a-z0-9]+/g) || [];
    const counts = {};
    for (const w of words) {
      if (stop && WF_STOP.has(w)) continue;
      if (w.length < 2) continue;
      counts[w] = (counts[w] || 0) + 1;
    }
    const rows = Object.entries(counts).sort((a,b) => b[1] - a[1]).slice(0, 100);
    const out = document.getElementById('wf-out');
    if (!rows.length) { out.textContent = 'No words found.'; return; }
    out.innerHTML = '<table class="tbl"><tr><th>Word</th><th>Count</th></tr>' +
      rows.map(r => '<tr><td>' + r[0] + '</td><td>' + r[1] + '</td></tr>').join('') + '</table>';
  }
""",
    },
    {
        "slug": "slug-generator",
        "name": "Slug Generator",
        "title": "URL Slug Generator - Make SEO-Friendly Slugs Online",
        "desc": "Turn any title into a clean, SEO-friendly URL slug: lowercase, hyphenated and safe for links.",
        "keywords": "slug generator, url slug, seo friendly url, permalink generator",
        "body": """
      <div class="card">
        <label for="sg-in">Title or text</label>
        <input id="sg-in" type="text" placeholder="e.g. 10 Best Free Online Tools!">
        <label for="sg-sep">Separator</label>
        <select id="sg-sep"><option value="-">Hyphen (-)</option><option value="_">Underscore (_)</option></select>
        <button class="btn" onclick="sgRun()">Generate slug</button>
        <div class="output" id="sg-out"></div>
      </div>
""",
        "script": """
  const sgIn = document.getElementById('sg-in');
  sgIn.addEventListener('input', sgRun);
  function sgRun() {
    const sep = document.getElementById('sg-sep').value;
    const slug = sgIn.value.toLowerCase().trim()
      .replace(/[^a-z0-9]+/g, sep)
      .replace(new RegExp('^' + sep + '+|' + sep + '+$', 'g'), '');
    document.getElementById('sg-out').innerHTML = slug
      ? '<code id="sg-res">' + slug + '</code> <button class="btn" onclick="sgCopy()">Copy</button>'
      : 'Type a title to see the slug.';
  }
  function sgCopy() {
    const t = document.getElementById('sg-res').textContent;
    if (navigator.clipboard) navigator.clipboard.writeText(t);
  }
""",
    },
    {
        "slug": "number-to-words",
        "name": "Number to Words",
        "title": "Number to Words Converter - Write Numbers in English Online",
        "desc": "Convert numbers into English words. Great for cheques, invoices and documents that need amounts in words.",
        "keywords": "number to words, number to words converter, write numbers in english, amount in words",
        "body": """
      <div class="card">
        <label for="nw-in">Number</label>
        <input id="nw-in" type="text" placeholder="e.g. 12500">
        <button class="btn" onclick="nwRun()">Convert</button>
        <div class="output" id="nw-out"></div>
      </div>
""",
        "script": """
  const NW_ONES = ['zero','one','two','three','four','five','six','seven','eight','nine','ten','eleven','twelve','thirteen','fourteen','fifteen','sixteen','seventeen','eighteen','nineteen'];
  const NW_TENS = ['','','twenty','thirty','forty','fifty','sixty','seventy','eighty','ninety'];
  function nwBelow1000(n) {
    if (n < 20) return NW_ONES[n];
    if (n < 100) return NW_TENS[Math.floor(n/10)] + (n%10 ? '-' + NW_ONES[n%10] : '');
    return NW_ONES[Math.floor(n/100)] + ' hundred' + (n%100 ? ' and ' + nwBelow1000(n%100) : '');
  }
  function nwRun() {
    const raw = document.getElementById('nw-in').value.replace(/[^0-9]/g, '');
    const out = document.getElementById('nw-out');
    if (!raw) { out.textContent = 'Enter a whole number.'; return; }
    let n = BigInt(raw);
    if (n > 999999999999n) { out.textContent = 'Please use a smaller number.'; return; }
    const parts = [];
    const scales = [[1000000000n,'billion'],[1000000n,'million'],[1000n,'thousand']];
    for (const [v, name] of scales) {
      if (n >= v) { parts.push(nwBelow1000(Number(n/v)) + ' ' + name); n = n % v; }
    }
    if (n > 0n) parts.push(nwBelow1000(Number(n)));
    out.textContent = parts.join(' ');
  }
""",
    },
    {
        "slug": "reverse-text",
        "name": "Reverse Text",
        "title": "Reverse Text Online - Flip Text, Words or Lines",
        "desc": "Reverse text by characters, words or lines instantly. Free online text reverser that works in your browser.",
        "keywords": "reverse text, text reverser, backwards text, reverse words online",
        "body": """
      <div class="card">
        <label for="rv-in">Your text</label>
        <textarea id="rv-in" rows="6" placeholder="Type or paste text..."></textarea>
        <label for="rv-mode">Reverse</label>
        <select id="rv-mode">
          <option value="chars">Characters (olleh)</option>
          <option value="words">Words (world hello)</option>
          <option value="lines">Lines</option>
        </select>
        <button class="btn" onclick="rvRun()">Reverse</button>
        <div class="output" id="rv-out"></div>
      </div>
""",
        "script": """
  function rvRun() {
    const t = document.getElementById('rv-in').value;
    const mode = document.getElementById('rv-mode').value;
    let r;
    if (mode === 'chars') r = t.split('').reverse().join('');
    else if (mode === 'words') r = t.split(/\\s+/).reverse().join(' ');
    else r = t.split('\\n').reverse().join('\\n');
    document.getElementById('rv-out').innerHTML = '<textarea rows="6" id="rv-res"></textarea>';
    document.getElementById('rv-res').value = r;
  }
""",
    },
    {
        "slug": "image-cropper",
        "name": "Image Cropper",
        "title": "Crop Image Online - Free Image Cropper",
        "desc": "Crop a JPG or PNG to any region by choosing the coordinates. Everything happens in your browser, so nothing is uploaded.",
        "keywords": "crop image online, image cropper, crop jpg, crop png free",
        "body": """
      <div class="card">
        <input id="cr-file" type="file" accept="image/*">
        <div class="row">
          <label>X <input id="cr-x" type="number" value="0" style="width:80px"></label>
          <label>Y <input id="cr-y" type="number" value="0" style="width:80px"></label>
          <label>Width <input id="cr-w" type="number" value="200" style="width:80px"></label>
          <label>Height <input id="cr-h" type="number" value="200" style="width:80px"></label>
        </div>
        <button class="btn" onclick="crRun()">Crop &amp; download</button>
        <div class="output" id="cr-out"></div>
      </div>
""",
        "script": """
  function crRun() {
    const file = document.getElementById('cr-file').files[0];
    const out = document.getElementById('cr-out');
    if (!file) { out.textContent = 'Choose an image first.'; return; }
    const img = new Image();
    img.onload = () => {
      const x = +document.getElementById('cr-x').value, y = +document.getElementById('cr-y').value;
      const w = +document.getElementById('cr-w').value, h = +document.getElementById('cr-h').value;
      const c = document.createElement('canvas');
      c.width = Math.max(1, Math.min(w, img.width - x));
      c.height = Math.max(1, Math.min(h, img.height - y));
      c.getContext('2d').drawImage(img, x, y, c.width, c.height, 0, 0, c.width, c.height);
      c.toBlob(b => {
        out.innerHTML = 'Cropped ' + c.width + ' x ' + c.height + ' px<br>' +
          '<a href="' + URL.createObjectURL(b) + '" download="cropped.png">Download cropped image</a>';
      });
    };
    img.onerror = () => out.textContent = 'Could not read that image.';
    img.src = URL.createObjectURL(file);
  }
""",
    },
    {
        "slug": "image-rotate-flip",
        "name": "Rotate & Flip Image",
        "title": "Rotate or Flip an Image Online - Free Image Rotator",
        "desc": "Rotate an image by 90, 180 or 270 degrees, or flip it horizontally or vertically. Free and browser-based.",
        "keywords": "rotate image online, flip image, rotate jpg, mirror image online",
        "body": """
      <div class="card">
        <input id="rf-file" type="file" accept="image/*">
        <div class="row">
          <button class="btn" onclick="rfDo(90)">Rotate 90°</button>
          <button class="btn" onclick="rfDo(180)">Rotate 180°</button>
          <button class="btn" onclick="rfDo(270)">Rotate 270°</button>
          <button class="btn" onclick="rfDo('h')">Flip horizontal</button>
          <button class="btn" onclick="rfDo('v')">Flip vertical</button>
        </div>
        <div class="output" id="rf-out"></div>
      </div>
""",
        "script": """
  function rfDo(mode) {
    const file = document.getElementById('rf-file').files[0];
    const out = document.getElementById('rf-out');
    if (!file) { out.textContent = 'Choose an image first.'; return; }
    const img = new Image();
    img.onload = () => {
      const c = document.createElement('canvas');
      const ctx = c.getContext('2d');
      if (mode === 'h' || mode === 'v') {
        c.width = img.width; c.height = img.height;
        if (mode === 'h') { ctx.translate(img.width, 0); ctx.scale(-1, 1); }
        else { ctx.translate(0, img.height); ctx.scale(1, -1); }
        ctx.drawImage(img, 0, 0);
      } else {
        const swap = mode === 90 || mode === 270;
        c.width = swap ? img.height : img.width;
        c.height = swap ? img.width : img.height;
        ctx.translate(c.width/2, c.height/2);
        ctx.rotate(mode * Math.PI / 180);
        ctx.drawImage(img, -img.width/2, -img.height/2);
      }
      c.toBlob(b => {
        out.innerHTML = '<a href="' + URL.createObjectURL(b) + '" download="rotated.png">Download image</a>';
      });
    };
    img.onerror = () => out.textContent = 'Could not read that image.';
    img.src = URL.createObjectURL(file);
  }
""",
    },
    {
        "slug": "image-color-picker",
        "name": "Image Color Picker",
        "title": "Image Color Picker - Get HEX & RGB From Any Image",
        "desc": "Upload an image and click anywhere to read the exact colour as HEX, RGB and HSL. Runs in your browser.",
        "keywords": "image color picker, eyedropper online, get color from image, hex color picker",
        "body": """
      <div class="card">
        <input id="cp-file" type="file" accept="image/*">
        <div id="cp-holder" style="margin-top:12px"></div>
        <div class="output" id="cp-out">Choose an image, then tap it to read the colour.</div>
      </div>
""",
        "script": """
  function cpHex(r,g,b) {
    return '#' + [r,g,b].map(v => v.toString(16).padStart(2,'0')).join('').toUpperCase();
  }
  document.getElementById('cp-file').addEventListener('change', function() {
    const file = this.files[0];
    const holder = document.getElementById('cp-holder');
    if (!file) return;
    const img = new Image();
    img.onload = () => {
      holder.innerHTML = '';
      const c = document.createElement('canvas');
      const max = 320;
      const scale = Math.min(1, max / img.width);
      c.width = img.width * scale; c.height = img.height * scale;
      const ctx = c.getContext('2d');
      ctx.drawImage(img, 0, 0, c.width, c.height);
      c.style.cursor = 'crosshair'; c.style.maxWidth = '100%';
      c.addEventListener('click', e => {
        const rect = c.getBoundingClientRect();
        const x = Math.floor((e.clientX - rect.left) * (c.width / rect.width));
        const y = Math.floor((e.clientY - rect.top) * (c.height / rect.height));
        const d = ctx.getImageData(x, y, 1, 1).data;
        document.getElementById('cp-out').innerHTML =
          '<span style="display:inline-block;width:24px;height:24px;background:' + cpHex(d[0],d[1],d[2]) +
          ';vertical-align:middle;border:1px solid #555"></span> ' +
          '<strong>' + cpHex(d[0],d[1],d[2]) + '</strong> &middot; rgb(' + d[0] + ', ' + d[1] + ', ' + d[2] + ')';
      });
      holder.appendChild(c);
    };
    img.src = URL.createObjectURL(file);
  });
""",
    },
    {
        "slug": "image-to-base64",
        "name": "Image to Base64",
        "title": "Image to Base64 Converter - Encode Images Online",
        "desc": "Convert a JPG or PNG into a Base64 data URI you can paste straight into HTML or CSS. Nothing is uploaded.",
        "keywords": "image to base64, base64 encode image, data uri generator, png to base64",
        "body": """
      <div class="card">
        <input id="b64-file" type="file" accept="image/*">
        <button class="btn" onclick="b64Run()">Encode</button>
        <div class="output" id="b64-out"></div>
      </div>
""",
        "script": """
  function b64Run() {
    const file = document.getElementById('b64-file').files[0];
    const out = document.getElementById('b64-out');
    if (!file) { out.textContent = 'Choose an image first.'; return; }
    const reader = new FileReader();
    reader.onload = () => {
      const uri = reader.result;
      out.innerHTML = '<textarea rows="6" id="b64-res"></textarea><br>' +
        '<span class="muted">' + Math.round(uri.length/1024) + ' KB of text</span> ' +
        '<button class="btn" onclick="b64Copy()">Copy</button>';
      document.getElementById('b64-res').value = uri;
    };
    reader.readAsDataURL(file);
  }
  function b64Copy() {
    const el = document.getElementById('b64-res');
    el.select();
    document.execCommand('copy');
  }
""",
    },
    {
        "slug": "favicon-generator",
        "name": "Favicon Generator",
        "title": "Favicon Generator - Create a Favicon From Any Image",
        "desc": "Turn a PNG or JPG into a 32x32 favicon. Download the .png and add it to your site in one line.",
        "keywords": "favicon generator, create favicon, 32x32 png, website icon generator",
        "body": """
      <div class="card">
        <input id="fv-file" type="file" accept="image/*">
        <button class="btn" onclick="fvRun()">Make favicon</button>
        <div class="output" id="fv-out"></div>
      </div>
""",
        "script": """
  function fvRun() {
    const file = document.getElementById('fv-file').files[0];
    const out = document.getElementById('fv-out');
    if (!file) { out.textContent = 'Choose an image first.'; return; }
    const img = new Image();
    img.onload = () => {
      const c = document.createElement('canvas');
      c.width = 32; c.height = 32;
      const ctx = c.getContext('2d');
      const side = Math.min(img.width, img.height);
      const sx = (img.width - side) / 2, sy = (img.height - side) / 2;
      ctx.drawImage(img, sx, sy, side, side, 0, 0, 32, 32);
      c.toBlob(b => {
        out.innerHTML = '<img src="' + URL.createObjectURL(b) + '" width="32" height="32" alt="favicon preview"> ' +
          '<a href="' + URL.createObjectURL(b) + '" download="favicon.png">Download favicon.png</a>' +
          '<p class="muted">Add to your HTML head: &lt;link rel="icon" href="/favicon.png"&gt;</p>';
      });
    };
    img.onerror = () => out.textContent = 'Could not read that image.';
    img.src = URL.createObjectURL(file);
  }
""",
    },
    {
        "slug": "meme-generator",
        "name": "Meme Generator",
        "title": "Meme Generator - Add Top & Bottom Text to an Image",
        "desc": "Upload a photo, add top and bottom captions and download the meme as a PNG. No sign-up, no upload to a server.",
        "keywords": "meme generator, add text to image, meme maker online, caption image",
        "body": """
      <div class="card">
        <input id="mm-file" type="file" accept="image/*">
        <label for="mm-top">Top text</label>
        <input id="mm-top" type="text" placeholder="TOP TEXT">
        <label for="mm-bottom">Bottom text</label>
        <input id="mm-bottom" type="text" placeholder="BOTTOM TEXT">
        <label for="mm-size">Font size: <span id="mm-sizev">48</span></label>
        <input id="mm-size" type="range" min="16" max="96" value="48">
        <button class="btn" onclick="mmRun()">Generate meme</button>
        <div class="output" id="mm-out"></div>
      </div>
""",
        "script": """
  const mmSize = document.getElementById('mm-size');
  mmSize.addEventListener('input', () => document.getElementById('mm-sizev').textContent = mmSize.value);
  function mmText(ctx, text, y, size, w) {
    if (!text) return;
    ctx.font = 'bold ' + size + 'px Impact, sans-serif';
    ctx.textAlign = 'center';
    ctx.lineWidth = Math.max(2, size / 12);
    ctx.strokeStyle = 'black';
    ctx.fillStyle = 'white';
    ctx.strokeText(text.toUpperCase(), w/2, y);
    ctx.fillText(text.toUpperCase(), w/2, y);
  }
  function mmRun() {
    const file = document.getElementById('mm-file').files[0];
    const out = document.getElementById('mm-out');
    if (!file) { out.textContent = 'Choose an image first.'; return; }
    const img = new Image();
    img.onload = () => {
      const c = document.createElement('canvas');
      c.width = img.width; c.height = img.height;
      const ctx = c.getContext('2d');
      ctx.drawImage(img, 0, 0);
      const size = +mmSize.value;
      mmText(ctx, document.getElementById('mm-top').value, size + 10, size, c.width);
      mmText(ctx, document.getElementById('mm-bottom').value, c.height - 15, size, c.width);
      c.toBlob(b => {
        out.innerHTML = '<a href="' + URL.createObjectURL(b) + '" download="meme.png">Download meme</a>';
      });
    };
    img.onerror = () => out.textContent = 'Could not read that image.';
    img.src = URL.createObjectURL(file);
  }
""",
    },
    {
        "slug": "uuid-generator",
        "name": "UUID Generator",
        "title": "UUID Generator - Generate v4 UUIDs Online",
        "desc": "Generate random version 4 UUIDs, one or many at a time, ready to copy. Uses the browser's secure random generator.",
        "keywords": "uuid generator, generate uuid, guid generator, random uuid v4",
        "body": """
      <div class="card">
        <label for="uu-n">How many</label>
        <input id="uu-n" type="number" value="5" min="1" max="100">
        <button class="btn" onclick="uuRun()">Generate</button>
        <div class="output" id="uu-out"></div>
      </div>
""",
        "script": """
  function uuMake() {
    if (crypto.randomUUID) return crypto.randomUUID();
    const b = crypto.getRandomValues(new Uint8Array(16));
    b[6] = (b[6] & 0x0f) | 0x40;
    b[8] = (b[8] & 0x3f) | 0x80;
    const h = Array.from(b).map(x => x.toString(16).padStart(2,'0')).join('');
    return h.slice(0,8) + '-' + h.slice(8,12) + '-' + h.slice(12,16) + '-' + h.slice(16,20) + '-' + h.slice(20);
  }
  function uuRun() {
    const n = Math.max(1, Math.min(100, +document.getElementById('uu-n').value || 1));
    const list = Array.from({length:n}, uuMake);
    document.getElementById('uu-out').innerHTML =
      '<textarea rows="' + Math.min(12, n) + '" id="uu-res"></textarea>';
    document.getElementById('uu-res').value = list.join('\\n');
  }
""",
    },
    {
        "slug": "json-to-csv",
        "name": "JSON to CSV",
        "title": "JSON to CSV Converter - Convert JSON Arrays Online",
        "desc": "Paste a JSON array of objects and get a CSV file back. Handles nested values by flattening them into columns.",
        "keywords": "json to csv, convert json to csv, json csv converter online",
        "body": """
      <div class="card">
        <label for="jc-in">JSON array</label>
        <textarea id="jc-in" rows="8" placeholder='[{"name":"A","age":30},{"name":"B","age":25}]'></textarea>
        <button class="btn" onclick="jcRun()">Convert to CSV</button>
        <div class="output" id="jc-out"></div>
      </div>
""",
        "script": """
  function jcCell(v) {
    if (v === null || v === undefined) return '';
    if (typeof v === 'object') v = JSON.stringify(v);
    const s = String(v);
    return /[",\\n]/.test(s) ? '"' + s.replace(/"/g, '""') + '"' : s;
  }
  function jcRun() {
    const out = document.getElementById('jc-out');
    let data;
    try { data = JSON.parse(document.getElementById('jc-in').value); }
    catch (e) { out.textContent = 'That is not valid JSON.'; return; }
    if (!Array.isArray(data) || !data.length) { out.textContent = 'Provide a non-empty JSON array of objects.'; return; }
    const cols = Array.from(new Set(data.flatMap(o => (o && typeof o === 'object') ? Object.keys(o) : [])));
    const lines = [cols.map(jcCell).join(',')];
    for (const row of data) lines.push(cols.map(c => jcCell(row ? row[c] : '')).join(','));
    const csv = lines.join('\\n');
    out.innerHTML = '<textarea rows="8" id="jc-res"></textarea><br>' +
      '<a download="data.csv" id="jc-dl">Download CSV</a>';
    document.getElementById('jc-res').value = csv;
    document.getElementById('jc-dl').href = 'data:text/csv;charset=utf-8,' + encodeURIComponent(csv);
  }
""",
    },
    {
        "slug": "html-minifier",
        "name": "HTML Minifier",
        "title": "HTML Minifier - Minify HTML Online",
        "desc": "Strip comments and extra whitespace from HTML to make the file smaller. A quick, browser-based minifier.",
        "keywords": "html minifier, minify html online, compress html, html optimizer",
        "body": """
      <div class="card">
        <label for="hm-in">HTML</label>
        <textarea id="hm-in" rows="8" placeholder="<div>  <p>Hello</p>  </div>"></textarea>
        <button class="btn" onclick="hmRun()">Minify</button>
        <div class="output" id="hm-out"></div>
      </div>
""",
        "script": """
  function hmRun() {
    let s = document.getElementById('hm-in').value;
    const before = s.length;
    s = s.replace(/<!--[\\s\\S]*?-->/g, '');
    s = s.replace(/>\\s+</g, '><');
    s = s.replace(/\\s{2,}/g, ' ');
    s = s.trim();
    const out = document.getElementById('hm-out');
    out.innerHTML = '<textarea rows="8" id="hm-res"></textarea><br>' +
      '<span class="muted">' + before + ' → ' + s.length + ' characters (' +
      Math.max(0, Math.round((1 - s.length/before) * 100)) + '% smaller)</span>';
    document.getElementById('hm-res').value = s;
  }
""",
    },
    {
        "slug": "css-minifier",
        "name": "CSS Minifier",
        "title": "CSS Minifier - Minify CSS Online",
        "desc": "Remove comments and unnecessary whitespace from CSS to shrink the file. Fast and browser-based.",
        "keywords": "css minifier, minify css online, compress css, css optimizer",
        "body": """
      <div class="card">
        <label for="cm-in">CSS</label>
        <textarea id="cm-in" rows="8" placeholder="body {  color: red;  }"></textarea>
        <button class="btn" onclick="cmRun()">Minify</button>
        <div class="output" id="cm-out"></div>
      </div>
""",
        "script": """
  function cmRun() {
    let s = document.getElementById('cm-in').value;
    const before = s.length;
    s = s.replace(/\\/\\*[\\s\\S]*?\\*\\//g, '');
    s = s.replace(/\\s+/g, ' ');
    s = s.replace(/\\s*([{}:;,>])\\s*/g, '$1');
    s = s.replace(/;}/g, '}');
    s = s.trim();
    const out = document.getElementById('cm-out');
    out.innerHTML = '<textarea rows="8" id="cm-res"></textarea><br>' +
      '<span class="muted">' + before + ' → ' + s.length + ' characters (' +
      Math.max(0, Math.round((1 - s.length/before) * 100)) + '% smaller)</span>';
    document.getElementById('cm-res').value = s;
  }
""",
    },
    {
        "slug": "random-name-picker",
        "name": "Random Name Picker",
        "title": "Random Name Picker - Pick a Random Winner Online",
        "desc": "Paste a list of names and pick one at random. Handy for giveaways, classrooms and team decisions.",
        "keywords": "random name picker, random winner picker, pick a name, random picker",
        "body": """
      <div class="card">
        <label for="rp-in">Names (one per line)</label>
        <textarea id="rp-in" rows="8" placeholder="Ali&#10;Sara&#10;Rahim"></textarea>
        <label><input type="checkbox" id="rp-no"> Don't repeat previous winner</label>
        <button class="btn" onclick="rpRun()">Pick one</button>
        <div class="output" id="rp-out"></div>
      </div>
""",
        "script": """
  let rpLast = null;
  function rpRun() {
    let names = document.getElementById('rp-in').value.split('\\n').map(s => s.trim()).filter(Boolean);
    if (!names.length) { document.getElementById('rp-out').textContent = 'Add some names first.'; return; }
    if (document.getElementById('rp-no').checked && names.length > 1) names = names.filter(n => n !== rpLast);
    const pick = names[Math.floor(Math.random() * names.length)];
    rpLast = pick;
    document.getElementById('rp-out').innerHTML = '<strong style="font-size:1.4em">' + pick + '</strong>';
  }
""",
    },
    {
        "slug": "dice-roller",
        "name": "Dice Roller",
        "title": "Dice Roller Online - Roll Virtual Dice",
        "desc": "Roll one or more six-sided dice online. Great for board games, RPGs and quick decisions.",
        "keywords": "dice roller, roll dice online, virtual dice, d6 roller",
        "body": """
      <div class="card">
        <label for="dr-n">Number of dice</label>
        <input id="dr-n" type="number" value="2" min="1" max="20">
        <button class="btn" onclick="drRun()">Roll</button>
        <div class="output" id="dr-out"></div>
      </div>
""",
        "script": """
  function drRun() {
    const n = Math.max(1, Math.min(20, +document.getElementById('dr-n').value || 1));
    const rolls = Array.from({length:n}, () => 1 + Math.floor(Math.random() * 6));
    const total = rolls.reduce((a,b) => a+b, 0);
    document.getElementById('dr-out').innerHTML =
      '<strong style="font-size:1.4em">' + rolls.join('  ') + '</strong><br>Total: ' + total;
  }
""",
    },
    {
        "slug": "coin-flip",
        "name": "Coin Flip",
        "title": "Coin Flip Online - Heads or Tails",
        "desc": "Flip a virtual coin and get heads or tails instantly. Perfect for settling a quick decision.",
        "keywords": "coin flip, heads or tails, flip a coin online, virtual coin toss",
        "body": """
      <div class="card">
        <button class="btn" onclick="cfRun()">Flip coin</button>
        <div class="output" id="cf-out"></div>
      </div>
""",
        "script": """
  function cfRun() {
    const r = Math.random() < 0.5 ? 'Heads' : 'Tails';
    document.getElementById('cf-out').innerHTML = '<strong style="font-size:1.6em">' + r + '</strong>';
  }
""",
    },
    {
        "slug": "emoji-picker",
        "name": "Emoji Picker",
        "title": "Emoji Picker - Copy Emojis Instantly",
        "desc": "Browse a grid of common emojis and copy any of them with one tap. Works on any device.",
        "keywords": "emoji picker, copy emoji, emoji list, emoji keyboard online",
        "body": """
      <div class="card">
        <div id="ep-grid" class="row"></div>
        <div class="output" id="ep-out">Tap an emoji to copy it.</div>
      </div>
""",
        "script": """
  const EP = '😀 😃 😄 😁 😆 😅 😂 🤣 😊 😇 🙂 😉 😍 🥰 😘 😜 😎 🤩 🥳 😏 😢 😭 😤 😡 🤔 🤗 🤭 🤫 😴 🤤 😱 🤯 🥺 😬 🙄 😌 👍 👎 👏 🙌 🤝 💪 🙏 ✌️ 🤞 👌 👋 🖐️ ✨ ⭐ 🌟 💫 🔥 💧 ❤️ 🧡 💛 💚 💙 💜 🖤 🤍 💔 💯 ✅ ❌ ⚠️ ❓ ❗ 🎉 🎊 🎁 🎂 🍕 🍔 🍟 🍎 🍌 🍇 ☕ 🍵 🍦 🍫 🌞 🌝 🌚 🌈 ☁️ 🌧️ ❄️ ⚡ 🌊 🌸 🌹 🌻 🐶 🐱 🐭 🐰 🦊 🐻 🐼 🐨 🦁 🐮 🐷 🐸 🐵 🐔 🐧 🐦 🦄 🐝 🦋 🚀 ✈️ 🚗 🚕 🚌 🚲 ⚽ 🏀 🎾 🎮 🎸 🎧 📱 💻 ⌨️ 🖱️ 📷 🔋 💡 🔑 🔒 📌 📎 📖 📝 ✏️ 📅 ⏰ 💰 💳 🛒 🎯 🏆 🥇 🥈 🥉 🎓 🏠 🏢 🗺️ 🧭 🧪 🔬 🩺 💊 🌍 🌎 🌏 🕌 🕋 📿'.split(' ');
  (function() {
    const grid = document.getElementById('ep-grid');
    grid.innerHTML = EP.map(e => '<button class="btn" style="font-size:1.4em" data-e="' + e + '">' + e + '</button>').join('');
    grid.addEventListener('click', ev => {
      const e = ev.target.getAttribute && ev.target.getAttribute('data-e');
      if (!e) return;
      if (navigator.clipboard) navigator.clipboard.writeText(e);
      document.getElementById('ep-out').innerHTML = 'Copied: <strong style="font-size:1.5em">' + e + '</strong>';
    });
  })();
""",
    },
]

