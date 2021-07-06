function flip_card()
{
	let mdfc = document.getElementById("mdfc");
	let src = mdfc.src;
	var uri_dict = {"front_uri": mdfc.getAttribute("data-front"), 
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

function select_set()
{
	let select = document.getElementsByName("set-select");
	let generate_button = document.getElementById("generate-button");
	let set_icon = document.getElementById("set-icon");

	const URI = "https://api.scryfall.com//sets//" + select[0].value;
	const Http = new XMLHttpRequest();

	Http.open("GET", URI);
	Http.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
	Http.send();

	Http.onreadystatechange = (e) => {
		json = JSON.parse(Http.responseText);
		set_icon.src = json["icon_svg_uri"];
	}

	if (select[0].value == "Select a Set")
	{
		generate_button.disabled = true;
	}
	else
	{
		generate_button.disabled = false;
	}
}