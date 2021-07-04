function flip(uri_dict)
{
	console.log("called card flip")
	let mdfc = document.getElementById("mdfc");
	let src = mdfc.src;

	if (src == uri_dict["front_uri"])
	{
		mdfc.src = uri_dict["back_uri"]
	}
	else
	{
		mdfc.src = uri_dict["front_uri"]
	}
}