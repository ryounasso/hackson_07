const g_elementDivJoinScreen = document.getElementById("div_join_screen");
const g_elementDivChatScreen = document.getElementById("div_chat_screen");
const g_elementInputUserName = document.getElementById("input_username");
const g_elementInputRoomName = document.getElementById("input_roomname");

//memo定数定義
const memo1 = document.getElementById("memo1");
const memo2 = document.getElementById("memo2");
const memo3 = document.getElementById("memo3");
const memo4 = document.getElementById("memo4");
const memo5 = document.getElementById("memo5");
const memo6 = document.getElementById("memo6");
const memo7 = document.getElementById("memo7");
const memo8 = document.getElementById("memo8");
const memo9 = document.getElementById("memo9");

const stamp = document.getElementById("stamp")

const g_elementTextUserName = document.getElementById("text_username");
const g_elementTextRoomName = document.getElementById("text_roomname");

const g_elementInputMessage = document.getElementById("input_message");
const g_elementListMessage = document.getElementById("list_message");

const imgListElemnt = document.getElementById("image_space");

// WebSocketオブジェクト
let ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
const g_socket = new WebSocket(
  // ws_scheme + "://" + window.location.host + "/wss/chat/"
  ws_scheme + "://" + window.location.host + "/ws/chat/"
  // ws_scheme + "://guarded-eyrie-48747.herokuapp.com/" + "ws/chat/"
);
const g_socket_image = new WebSocket(
  ws_scheme + "://" + window.location.host + "/ws/chat/"
  // ws_scheme + "://guarded-eyrie-48747.herokuapp.com/" + "ws/chat/"
);

// 「Join」ボタンを押すと呼ばれる関数
function onsubmitButton_JoinChat() {
  // ユーザー名
  let strInputUserName = g_elementInputUserName.value;
  if (!strInputUserName) {
    return;
  }
  g_elementTextUserName.value = strInputUserName;

  // ルーム名
  let strInputRoomName = g_elementInputRoomName.value;
  g_elementTextRoomName.value = strInputRoomName;
  if(strInputRoomName==="hallA"){
    g_elementTextRoomName.classList.add("button1")
  }
  if(strInputRoomName==="hallB"){
    g_elementTextRoomName.classList.add("button2")
  }
  if(strInputRoomName==="hallC"){
    g_elementTextRoomName.classList.add("button3")
  }
  if(strInputRoomName==="room1"){
    g_elementTextRoomName.classList.add("button4")
  }
  if(strInputRoomName==="roo2"){
    g_elementTextRoomName.classList.add("button4")
  }

  // サーバーに"join"を送信
  g_socket.send(
    JSON.stringify({
      data_type: "join",
      username: strInputUserName,
      roomname: strInputRoomName,
    })
  );

  // 画面の切り替え
  g_elementDivJoinScreen.style.display = "none"; // 参加画面の非表示
  g_elementDivChatScreen.style.display = "block"; // チャット画面の表示
}

// 「Leave Chat.」ボタンを押すと呼ばれる関数
function onclickButton_LeaveChat()
{
    // メッセージリストのクリア
    // while( g_elementListMessage.firstChild )
    // {
    //     g_elementListMessage.removeChild( g_elementListMessage.firstChild );
    // }

  // ユーザー名
  g_elementTextUserName.value = "";

  // サーバーに"leave"を送信
  g_socket.send(JSON.stringify({ data_type: "leave" }));

  // 画面の切り替え
  g_elementDivChatScreen.style.display = "none"; // チャット画面の非表示
  g_elementDivJoinScreen.style.display = "flex"; // 参加画面の表示

  memo1.innerHTML = "";
  memo2.innerHTML = "";
  memo3.innerHTML = "";
  memo4.innerHTML = "";
  memo5.innerHTML = "";
  memo6.innerHTML = "";
  memo7.innerHTML = "";
  memo8.innerHTML = "";
  memo9.innerHTML = "";
  imgListElemnt.innerHTML = "";
  if(g_elementTextRoomName.classList.contains("button1") ) {
    g_elementTextRoomName.classList.remove("button1");
  } else if (g_elementTextRoomName.classList.contains("button2")) {
    g_elementTextRoomName.classList.remove("button2");
  } else if (g_elementTextRoomName.classList.contains("button3")) {
    g_elementTextRoomName.classList.remove("button3");
  } else if (g_elementTextRoomName.classList.contains("button4")) {
    g_elementTextRoomName.classList.remove("button4");
  }
}

// 画像をBase64に変換
let imageBase64 = "";

const imageInput = document.getElementById("input_image");

imageInput.addEventListener("change", (e) => {
  // 画像ファイルを取得し、画像データ(URL)を変数に代入
  const imageFile = e.target.files[0];
  const imageURL = window.URL.createObjectURL(imageFile);
  // img要素を作成し、src属性に画像のURLを指定
  const imageElement = new Image();
  imageElement.src = imageURL;

  imageElement.onload = function () {
    // canvas要素を作成し、img要素を描画
    const canvasElement = document.createElement("canvas");
    canvasElement.width = imageElement.width;
    canvasElement.height = imageElement.height;
    const canvasContext = canvasElement.getContext("2d");
    canvasContext.drawImage(imageElement, 0, 0);
    // canvas要素をbase64形式に変換
    imageBase64 = canvasElement.toDataURL("image/png");
  };
});

// 「Send」ボタンを押したときの処理
function onsubmitButton_Send()
{
    // 送信用テキストHTML要素からメッセージ文字列の取得
    let strMessage = g_elementInputMessage.value;
    if( !strMessage )
    {
        return;
    }

    // WebSocketを通したメッセージの送信
    g_socket.send( JSON.stringify( { "message": strMessage, "member": countMember, } ) );

    // 送信用テキストHTML要素の中身のクリア
    g_elementInputMessage.value = "";
}

function onsubmitButton_sendImage(){
    if( !imageBase64 ){
        return;
    }
    let strMessage = "null";
    g_socket.send( JSON.stringify({ "message": strMessage, "image": imageBase64, "member": countMember, }) );
    imageInput.value = "";
    imageBase64 = "";
}

/** 重複チェック用配列 */
let randoms = [];
/** 最小値と最大値 */
let min = 1,
  max = 9;

/** min以上max以下の整数値の乱数を返す */
function intRandom(min, max) {
  return Math.floor(Math.random() * (max - min + 1)) + min;
}
let countMember = 0;
// WebSocketからメッセージ受信時の処理
g_socket.onmessage = ( event ) =>
{
    // 自身がまだ参加していないときは、無視。
    if( !g_elementTextUserName.value )
    {
        return;
    }

    // テキストデータをJSONデータにデコード
    let data = JSON.parse( event.data );

    // メッセージの整形
    let strMessage = data["message"];
    if(data["username"] != "*system*"){
        strMessage = " user " + data["username"] + '<br>' + data["message"];
    }
    // let strMessage = " user " + data["username"] + data["message"];
    let flag = data["message"];
//     let strMessage = data["datetime"] + " - [" + data["username"] + "] " + data["message"];
    // let flag = data["message"];
    countMember = data["member"];

    // 拡散されたメッセージをメッセージリストに追加
    let elementLi = document.createElement( "p" );
    let tmp =[];



    /** 重複チェックしながら乱数作成 */
    elementLi.textContent = strMessage;
    if (flag != 'null'){
        let c
        for(i = min; i <= max; i++){
            if (c===false){
                if(randoms.length===9){
                    randoms.splice(0)
                }
                break
            }
            while(true){
               tmp = intRandom(min, max);
              if(!randoms.includes(tmp)){
                let memo =eval("memo"+tmp)
                console.log(memo)
                randoms.push(tmp);
                memo.innerHTML =  elementLi.textContent; // リストの一番上に追加
                c=false
                break;
            }
        }
      }
    }
    if (data["image"] != "null") {
      // 受信した画像をimg要素としてmessageに組み込む
      const messageImage = document.createElement("img");
      messageImage.setAttribute("src", data["image"]);
      imgListElemnt.appendChild(messageImage);
      c = false;
  }
  //g_elementListMessage.append( elementLi );    // リストの一番下に追加
  var imgarea = document.getElementById("audience_images");
  imgarea.innerHTML = "";

  for(let i = 0;i < countMember; i++){
    var imgElement = document.createElement('img');
    imgElement.src = "../../../static/images/sittingwoman-removebg-preview.png";
    imgarea.appendChild(imgElement);
}
  }

g_socket.onclose = ( event ) =>
{
    // ウェブページを閉じたとき以外のWebSocketクローズは想定外
    console.error( "Unexpected : Chat socket closed." );
};

