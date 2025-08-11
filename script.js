
const textInput = document.getElementById('textInput');
const voiceSelect = document.getElementById('voiceSelect');
const rate = document.getElementById('rate');
const pitch = document.getElementById('pitch');
const speakBtn = document.getElementById('speakBtn');
const stopBtn = document.getElementById('stopBtn');
const clearBtn = document.getElementById('clearBtn');

let voices = [];
function populateVoices() {
  voices = speechSynthesis.getVoices();
  voiceSelect.innerHTML = voices.map((v,i)=>`<option value="${i}">${v.name} (${v.lang})</option>`).join('');
}
speechSynthesis.onvoiceschanged = populateVoices;

function speakText(){
  const utter = new SpeechSynthesisUtterance(textInput.value);
  const v = voices[voiceSelect.value];
  if(v) utter.voice = v;
  utter.rate = parseFloat(rate.value);
  utter.pitch = parseFloat(pitch.value);
  let audio = new Audio('https://www.soundjay.com/button/beep-07.wav');
  audio.play().then(()=>speechSynthesis.speak(utter));
}
speakBtn.addEventListener('click', speakText);
stopBtn.addEventListener('click', ()=>speechSynthesis.cancel());
clearBtn.addEventListener('click', ()=>textInput.value = '');

// Starfield animation
const canvas = document.getElementById('starfield');
const ctx = canvas.getContext('2d');
let stars = [];
function resize(){canvas.width = window.innerWidth; canvas.height = window.innerHeight;}
window.addEventListener('resize', resize);
resize();
for(let i=0;i<200;i++){
  stars.push({x:Math.random()*canvas.width,y:Math.random()*canvas.height,z:Math.random()*canvas.width});
}
function animate(){
  ctx.fillStyle='black';
  ctx.fillRect(0,0,canvas.width,canvas.height);
  ctx.fillStyle='white';
  for(let s of stars){
    s.z -= 2;
    if(s.z <= 0) s.z = canvas.width;
    let k = 128.0 / s.z;
    let px = s.x * k + canvas.width/2;
    let py = s.y * k + canvas.height/2;
    if(px>=0 && px<=canvas.width && py>=0 && py<=canvas.height){
      let size = (1 - s.z / canvas.width) * 3;
      ctx.fillRect(px,py,size,size);
    }
  }
  requestAnimationFrame(animate);
}
animate();

// Intro animation logic
setTimeout(()=>{
  document.getElementById('intro').classList.add('hidden');
  document.querySelector('main').classList.remove('hidden');
}, 3000);

// Fail-safe: always reveal UI after max 4s
setTimeout(()=>{
  document.getElementById('intro').classList.add('hidden');
  document.querySelector('main').classList.remove('hidden');
}, 4000);
