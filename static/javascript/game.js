function write_form_for_card(label, url, type) {
    document.write(
        `<form method='POST' name='${type.toUpperCase()}' action='${url}'>` +
        `<input type='hidden' name='${type}' value='${label}'></form>`
    );
}

function write_alink_for_card(label, no, type) {
    document.write(
        `<li><a href="javascript:${type.toUpperCase()}[${no}].submit()">${label}</a></li>`
    );
}

function write_non_alink_for_card(label) {
    document.write(
        `<li>${label}</li>`
    );
}

function write_cards(cardsAndFlags, type, url) {
    let cardsAndFlagsOfType = cardsAndFlags[type];
    for (let i = 0; i < cardsAndFlagsOfType.length; i++) {
        let card_and_flag = cardsAndFlagsOfType[i];
        let label = card_and_flag["label"];
        let isSelected = Number(card_and_flag["is_selected"]);
        write_form_for_card(label, url, type);
        if (!isSelected) {
            write_alink_for_card(label, i, type);
        } else {
            write_non_alink_for_card(label);
        }
    }
}
