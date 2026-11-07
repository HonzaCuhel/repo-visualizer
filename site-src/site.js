(()=>{
 const command=document.getElementById('install-command');
 if(!command)return;
 const buttons=[...document.querySelectorAll('[data-install-agent]')];
 const base='npx skills add HonzaCuhel/repo-visualizer --skill repo-visualizer';
 for(const button of buttons)button.addEventListener('click',()=>{
  const value=button.dataset.installAgent;
  command.textContent=base+(value==='both'?' -a codex -a claude-code':' -a '+value);
  for(const item of buttons)item.setAttribute('aria-pressed',String(item===button));
  document.getElementById('install-feedback').textContent='Run inside your repository. Add -g to install for all your projects. Requires Node.js 22.20+.';
 });
 document.getElementById('copy-install').addEventListener('click',async()=>{
  try{await navigator.clipboard.writeText(command.textContent);document.getElementById('install-feedback').textContent='Installation command copied.'}
  catch{const range=document.createRange();range.selectNodeContents(command);const selection=getSelection();selection.removeAllRanges();selection.addRange(range);document.getElementById('install-feedback').textContent='Command selected. Copy it with your keyboard shortcut.'}
 });
})();
