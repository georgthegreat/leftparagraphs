document.onkeydown = navArr;

var arrowLeft = 0x27;
var arrowRight = 0x25;

//big thanks to ArtLebedev studio
function navArr(event)
{
	if (!document.getElementById) 
		return;
	var next = document.getElementById("NextLink");
	var prev = document.getElementById("PrevLink");
		
	if (window.event) 
		event = window.event;

	if (event.ctrlKey)
	{
		switch (event.keyCode)		  
		{
			case arrowLeft:
				if (next)
					document.location = next.href;
				break;
			case arrowRight:
				if (prev)
					document.location = prev.href;
				break;
		}
	}
	return;	 
}
