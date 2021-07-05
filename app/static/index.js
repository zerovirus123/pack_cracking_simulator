function flip_card()
{
	console.log("called card flip");
	let mdfc = document.getElementById("mdfc");
	let src = mdfc.src;
	let uri_dict = {"front_uri": mdfc.dataset.data_front, "back_uri": mdfc.dataset.data_back};

	console.log("Img src: " + src);
	console.log("Card dict: " + uri_dict);
	console.log(mdfc.dataset.data_front);
	console.log(mdfc.dataset.data_back);
	console.log(uri_dict["front_uri"]);
	console.log(uri_dict["back_uri"])

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