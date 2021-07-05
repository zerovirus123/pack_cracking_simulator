function flip_card(id)
{
	console.log("called card flip");
	let mdfc = document.getElementById("mdfc"+id);
	let src = mdfc.src;
	let uri_dict = {"front_uri": mdfc.dataset.front, "back_uri": mdfc.dataset.back};

	console.log("Img src: " + src);
	console.log("Card dict: " + uri_dict);
	console.log(mdfc.dataset.front);
	console.log(mdfc.dataset.back);
	console.log(uri_dict["front_uri"]);
	console.log(uri_dict["back_uri"])

	if (uri_dict["back_uri"] != "None"){
		if (src == uri_dict["front_uri"])
		{
			console.log("flip to back");
			mdfc.src = uri_dict["back_uri"]
		}
		else
		{
			console.log("flip to front");
			mdfc.src = uri_dict["front_uri"]
		}
	}
}