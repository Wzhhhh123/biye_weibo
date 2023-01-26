/*jQuery time*/
$(document).ready(function(){
	$("#accordian h3").click(function(){
        $('.active').removeClass('active');
        $(this).addClass('active');
		//slide up all the link lists
		$("#accordian ul ul").slideUp();
		//slide down the link list below the h3 clicked - only if its closed
		if(!$(this).next().is(":visible"))
		{
			$(this).next().slideDown();
		}
	})
    
    $('#accordian li a').click(function(){
       $('.submenu-active').removeClass('submenu-active');
       $(this).addClass('submenu-active');
    });
})