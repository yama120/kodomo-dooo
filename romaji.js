(function (root) {
  'use strict';

/* 地域ページのURLに使うローマ字の対応表。
   検索ページ（URLの書き換え）と生成スクリプトの両方から使うので、
   ブラウザでもNodeでも読める素のスクリプトにしてある。
   Airbnb（okayama-japan）・SUUMO（sc_okayamashikita）・食べログ（A3301）と同じく、
   URLに日本語は入れない。読み仮名は機械的に決められないので手で持つ。

   ★対応表に無い値が来たら slug() は例外を投げる。
     ビルドが止まるので、新しい市区町村・種目が増えたらここに追記すること。
     黙って変なURLを作るより、止めて気づけるほうが安全。 */

const PREF = {
  "北海道": "hokkaido", "青森県": "aomori", "岩手県": "iwate", "宮城県": "miyagi",
  "秋田県": "akita", "山形県": "yamagata", "福島県": "fukushima", "茨城県": "ibaraki",
  "栃木県": "tochigi", "群馬県": "gunma", "埼玉県": "saitama", "千葉県": "chiba",
  "東京都": "tokyo", "神奈川県": "kanagawa", "新潟県": "niigata", "富山県": "toyama",
  "石川県": "ishikawa", "福井県": "fukui", "山梨県": "yamanashi", "長野県": "nagano",
  "岐阜県": "gifu", "静岡県": "shizuoka", "愛知県": "aichi", "三重県": "mie",
  "滋賀県": "shiga", "京都府": "kyoto", "大阪府": "osaka", "兵庫県": "hyogo",
  "奈良県": "nara", "和歌山県": "wakayama", "鳥取県": "tottori", "島根県": "shimane",
  "岡山県": "okayama", "広島県": "hiroshima", "山口県": "yamaguchi", "徳島県": "tokushima",
  "香川県": "kagawa", "愛媛県": "ehime", "高知県": "kochi", "福岡県": "fukuoka",
  "佐賀県": "saga", "長崎県": "nagasaki", "熊本県": "kumamoto", "大分県": "oita",
  "宮崎県": "miyazaki", "鹿児島県": "kagoshima", "沖縄県": "okinawa",
};

/* 市区町村。同じ名前が複数の県にあっても、URLは /clubs/<県>/<市>/ なので衝突しない
   （港区は東京・大阪・名古屋にあるが、県が違えば別パスになる） */
const CITY = {
  "あきる野市": "akiruno", "あま市": "ama", "京都市": "kyoto", "今治市": "imabari",
  "伊丹市": "itami", "入間市": "iruma", "八幡市": "yawata", "八王子市": "hachioji",
  "刈谷市": "kariya", "千葉市": "chiba", "南城市": "nanjo", "南風原町": "haebaru",
  "糸満市": "itoman", "印西市": "inzai", "名古屋市": "nagoya", "名張市": "nabari",
  "堺市": "sakai", "大和市": "yamato", "大府市": "obu", "大阪市": "osaka",
  "奄美市": "amami", "姫路市": "himeji", "小郡市": "ogori", "山口市": "yamaguchi",
  "山陽小野田市": "sanyo-onoda", "岡崎市": "okazaki", "川崎市": "kawasaki",
  "帯広市": "obihiro", "広島市": "hiroshima", "春日井市": "kasugai", "春日市": "kasuga",
  "木更津市": "kisarazu", "札幌市": "sapporo", "板橋区": "itabashi", "柏市": "kashiwa",
  "水戸市": "mito", "江戸川区": "edogawa", "池田市": "ikeda", "沖縄市": "okinawa",
  "泉佐野市": "izumisano", "津島市": "tsushima", "清須市": "kiyosu", "渋谷区": "shibuya",
  "港区": "minato", "潮来市": "itako", "熊本市": "kumamoto", "白井市": "shiroi",
  "相模原市": "sagamihara", "神戸市": "kobe", "福井市": "fukui", "福山市": "fukuyama",
  "稲沢市": "inazawa", "箕面市": "minoh", "船橋市": "funabashi", "草津市": "kusatsu",
  "葛飾区": "katsushika", "薩摩川内市": "satsumasendai", "藤枝市": "fujieda",
  "西宮市": "nishinomiya", "豊田市": "toyota", "那覇市": "naha", "鎌倉市": "kamakura",
  "長久手市": "nagakute", "青森市": "aomori", "飯塚市": "iizuka", "高槻市": "takatsuki",
};

/* 種目。既存の sport-*.html のスラッグと合わせられるものは合わせている
   （sport-soccer.html ↔ soccer）。表記ゆれ（体操教室／運動教室／運動基礎など）は
   クラブが自分で入力した値なので、いまは統合せずそのまま面にする。 */
const SPORT = {
  "サッカー": "soccer", "ダンス": "dance", "ダブルダッチ": "double-dutch",
  "野球": "baseball", "バレーボール": "volleyball", "空手": "karate",
  "陸上": "athletics", "バスケットボール": "basketball", "テニス": "tennis",
  "スポーツリズムトレーニング": "rhythm-training", "体操教室": "gymnastics-school",
  "マルチスポーツ": "multi", "スポーツ鬼ごっこ": "onigokko",
  "運動能力向上スクール": "athletic-ability", "卓球": "table-tennis",
  "パーソナルレッスン": "personal", "体操、サッカー": "gymnastics-soccer",
  "運動基礎": "basic-exercise", "フラッグフットボール": "flag-football",
  "バトントワーリング": "baton", "チアダンス": "cheer-dance",
  "体育": "physical-education", "ブラジリアン柔術": "bjj", "テコンドー": "taekwondo",
  "運動教室": "exercise-class", "水泳": "swimming", "レスリング": "wrestling",
  "剣道": "kendo", "キッズ運動スクール": "kids-sports", "体操": "gymnastics",
};

/* 「南風原町、糸満市」「体操、サッカー」のように、1つの欄に複数入れているクラブがある。
   クラブのデータは勝手に直さず、生成側で分割して両方のページに載せる。 */
const splitMulti = (value) =>
  String(value || "").split(/[、,，・／\/]/).map((s) => s.trim()).filter(Boolean);

const TABLE = { pref: PREF, city: CITY, sport: SPORT };
const LABEL = { pref: "都道府県", city: "市区町村", sport: "種目" };

function slug(kind, name) {
  const hit = TABLE[kind][name];
  if (!hit) {
    throw new Error(
      `seo-romaji.mjs に ${LABEL[kind]}「${name}」のローマ字がありません。` +
      `${kind.toUpperCase()} に追記してから再実行してください。`,
    );
  }
  return hit;
}

  root.ChibiRomaji = { PREF: PREF, CITY: CITY, SPORT: SPORT, slug: slug, splitMulti: splitMulti };
})(typeof window !== 'undefined' ? window : globalThis);
