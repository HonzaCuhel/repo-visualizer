/* Browser-only playback clock. Export adapters seek the shared scene directly. */
(()=>{
 const player=window.repoPlayer;
 let frame=0,last=0;
 function pause(){cancelAnimationFrame(frame);player._setPlaying(false);last=0}
 function tick(now){
  if(!player.isPlaying)return;
  if(!last)last=now;
  const next=player.timeMs+now-last;last=now;
  if(next>=player.durationMs){window.renderAt(player.durationMs-.001);pause();return}
  window.renderAt(next);frame=requestAnimationFrame(tick);
 }
 window.repoClock={pause,toggle(){
  if(player.isPlaying){pause();return}
  if(player.timeMs>=player.durationMs-10)window.renderAt(0);
  player.setView('path');player._setPlaying(true);last=0;frame=requestAnimationFrame(tick);
 }};
})();
