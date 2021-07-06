function flip_card()
{
	let mdfc = document.getElementById("mdfc");
	let src = mdfc.src;
	let uri_dict = {"front_uri": mdfc.getAttribute("data-front"), 
	                "back_uri": mdfc.getAttribute("data-back")};

	if (src == uri_dict["front_uri"])
	{
		mdfc.src = uri_dict["back_uri"]
	}
	else
	{
		mdfc.src = uri_dict["front_uri"]
	}
}