function showMessage(txt){
	// document.getElementById('right_bottom').classList.add('hide');

    this.timer && clearTimeout(this.timer);
    var oDiv = document.getElementById('messageInfo');
    if(!oDiv){
      oDiv = document.createElement('div');
      oDiv.className = 'messageInfo';
      oDiv.id = 'messageInfo';
		


		
		
		
      document.getElementById('right1').appendChild(oDiv);
    }
    oDiv.innerHTML = '<div class="active" style="width: 350px;position: absolute;height: 100px;left: 264px;top: 58px;">'+'<span>'+txt+'</span>'+'</div>';
    oDiv.classList.remove('hide');//默认是显示
    this.timer = 
      setTimeout(function(){
      oDiv.classList.add('hide');
	// var t = document.getElementById("right_bottom");
	// t.classList.remove('hide');//2s后隐藏
    },2000)
}


function hotpotshow(){


}


