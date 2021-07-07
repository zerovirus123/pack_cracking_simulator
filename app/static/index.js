let cache = {};

let card = document.getElementById("card");
card.addEventListener("click", flipCard);

function flipCard()
{
	card.classList.toggle("flipCard");
}

function flip_card(card_id)
{
	let mdfc = document.getElementById("mdfc" + card_id);
	let src = mdfc.src;
	var uri_dict = {"front_uri": mdfc.getAttribute("data-front"), 
	                "back_uri": mdfc.getAttribute("data-back")};

	if (uri_dict["back_uri"] != "None"){
		if (src == uri_dict["front_uri"])
		{
			mdfc.src = uri_dict["back_uri"]
		}
		else
		{
			mdfc.src = uri_dict["front_uri"]
		}
	}
}

function select_set()
{
	const select = document.getElementsByName("set-select");
	let generate_button = document.getElementById("generate-button");
	let set_icon = document.getElementById("set-icon");
	let set_code = select[0].value;
	
	if (set_code == "Select a Set")
	{
		generate_button.disabled = true;
	}
	else
	{
		if (cache[set_code]){
			set_icon.src = cache[set_code];
		}
		else
		{
			const URI = "https://api.scryfall.com//sets//" + set_code;
			const Http = new XMLHttpRequest();
	
			Http.open("GET", URI);
			Http.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
			Http.send();
	
			Http.onreadystatechange = (e) => {
				json = JSON.parse(Http.responseText);
				set_icon.src = json["icon_svg_uri"];
				cache[set_code] = json["icon_svg_uri"]
			}
		}
		generate_button.disabled = false;
	}
}