// window.onload イベントを使用してページが完全に読み込まれた後に実行する
window.onload = function() {
    // おやつ候補画像のIDを取得
    for (var i = 0; i < foodList.length; i++) {
        var img_id = foodList[i]['label'];
        var img = document.getElementById(img_id);

        // 画像がクリックされたときの処理を設定
        img.addEventListener("click", createClickHandler_hood(img_id));
    }
    // 選択されたおやつ画像のIDを取得
    var selectedObj =  document.getElementById("img_food_selected");
    if (selectedObj) {
        selectedObj.addEventListener("click", createClickHandler_selected_hood(selectedObj));
    }
    // お世話候補画像のIDを取得
    for (var i=0; i < careList.length; i++) {
        var img_id = careList[i]['label'];
        var img = document.getElementById(img_id);

         // 画像がクリックされたときの処理を設定
         img.addEventListener("click", createClickHandler_care(img_id));
    }
    // 選択されたお世話画像のIDを取得
    for (var i=0; i < max_care; i++) {
        var selectedObj = document.getElementById("img_care_selected_" + i);
        if (selectedObj) {
            selectedObj.addEventListener("click", createClickHandler_selected_care(selectedObj, i));
        }
    }
}

// クリックハンドラを生成する関数(food)
function createClickHandler_hood(img_id) {
    return function() {
        var selectedObj =  document.getElementById("img_food_selected");
        if (selectedObj) {
            ; // 何もしない
        } else {
            var foodImageFileName = img_id + '.jpg';
            var foodImageSrc = './static/' + foodImageFileName;
            var imgElement = document.createElement("img");
            imgElement.src = foodImageSrc;
            imgElement.id = "img_food_selected";
            imgElement.style.position = "absolute";
            imgElement.style.top = "458px";
            imgElement.style.left = "145px";
            imgElement.style.width = "96px";
            imgElement.style.height = "auto";
            // <img>要素をドキュメントに追加
            document.body.appendChild(imgElement);
            imgElement.addEventListener("click", createClickHandler_selected_hood(imgElement));
        }    
    }
}

function createClickHandler_selected_hood(Obj) {
    return function() {
        document.body.removeChild(Obj);
    }
}

// クリックハンドラを生成する関数(care)
function createClickHandler_care(img_id) {
    return function() {
        var selected_cares_number = 0;
        for (var i = 0; i < max_care; i++) {
            var Check_id = 'img_care_selected_' + i;
            var CheckObj = document.getElementById(Check_id);
            if (CheckObj) {
                selected_cares_number += 1; // 選択されているお世話の数をカウント
            }
        }

        if (selected_cares_number < max_care) {
            // お世話画像を表示
            var careImageFileName = img_id + '.jpg';
            var careImageSrc = './static/' + careImageFileName;
            var imgElement = document.createElement("img");
            imgElement.src = careImageSrc;
            imgElement.id = "img_care_selected_" + selected_cares_number;
            imgElement.style.position = "absolute";
            var left_position = 370 + selected_cares_number * 114;
            imgElement.style.top = "496px";
            imgElement.style.left = left_position + "px";
            imgElement.style.width = "97px";
            imgElement.style.height = "auto";
            // <img>要素をドキュメントに追加
            document.body.appendChild(imgElement);
            imgElement.addEventListener("click", createClickHandler_selected_care(imgElement, selected_cares_number))

            // ゲート画像を表示
            var gateImageFileName = 'g_' + img_id + '.jpg';
            var gateImageSrc = './static/' + gateImageFileName;
            var imgElement = document.createElement("img");
            imgElement.src = gateImageSrc;
            imgElement.id = "img_gate_selected_" + selected_cares_number;
            imgElement.style.position = "absolute";
            var left_position = 366 + selected_cares_number * 114;
            imgElement.style.top = "90px";
            imgElement.style.left = left_position + "px";
            imgElement.style.width = "106px";
            imgElement.style.height = "auto";
            // <img>要素をドキュメントに追加
            document.body.appendChild(imgElement);
        } else {
            ; // 何もしない
        }
    }
}

function createClickHandler_selected_care(Obj, number) {
    return function() {
        var selected_cares_number = 0;
        for (var i = 0; i < max_care; i++) {
            var Check_id = 'img_care_selected_' + i;
            var CheckObj = document.getElementById(Check_id);
            if (CheckObj) {
                selected_cares_number += 1;
            }
        }
        // お世話画像を非表示
        document.body.removeChild(Obj);
        // ゲート画像を非表示
        var img_id = "img_gate_selected_" + number;
        var ImgElement = document.getElementById(img_id);
        document.body.removeChild(ImgElement);

        if (selected_cares_number != number+1) {
            for (var i = number+1; i < selected_cares_number; i++) {
                var Relocate_id = 'img_care_selected_' + i;
                var RelocateObj = document.getElementById(Relocate_id);
                var careImageSrc = RelocateObj.src
                var position = RelocateObj.style.position
                var top_position = RelocateObj.style.top
                var RelocateId = i-1
                var left_position = 370 + RelocateId * 114
                var width = RelocateObj.style.width
                var height = RelocateObj.style.height
                document.body.removeChild(RelocateObj); // 画像を一旦消去
                var imgElement = document.createElement("img"); // 画像要素を再生成
                imgElement.src = careImageSrc
                imgElement.id = "img_care_selected_" + RelocateId;
                imgElement.style.position = position;
                imgElement.style.top = top_position;
                imgElement.style.left = left_position + "px";
                imgElement.style.width = width;
                imgElement.style.height = height;
                // <img>要素をドキュメントに追加
                document.body.appendChild(imgElement);
                imgElement.addEventListener("click", createClickHandler_selected_care(imgElement, RelocateId))

                var Relocate_id = 'img_gate_selected_' + i;
                var RelocateObj = document.getElementById(Relocate_id);
                var gateImageSrc = RelocateObj.src
                var position = RelocateObj.style.position
                var top_position = RelocateObj.style.top
                var RelocateId = i-1
                var left_position = 366 + RelocateId * 114;
                var width = RelocateObj.style.width
                var height = RelocateObj.style.height
                document.body.removeChild(RelocateObj); // 画像を一旦消去
                var imgElement = document.createElement("img"); // 画像要素を再生成
                imgElement.src = gateImageSrc;
                imgElement.id = "img_gate_selected_" + RelocateId;
                imgElement.style.position = position;
                imgElement.style.top = top_position;
                imgElement.style.left = left_position + "px";
                imgElement.style.width = width;
                imgElement.style.height = height;
                // <img>要素をドキュメントに追加
                document.body.appendChild(imgElement);
            }
        }
    }
}
