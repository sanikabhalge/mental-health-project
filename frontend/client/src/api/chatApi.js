// export async function sendChatMessage(token, payload) {
//   const res = await fetch("http://localhost:8000/api/chat/message", {
//   method: "POST",
//   headers: {
//     "Content-Type": "application/json",
//   },
//   body: JSON.stringify({ text: text })


//   });

//   return res.json();
// }
const token = localStorage.getItem("token");

const res = await fetch("http://localhost:8000/api/chat/message", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
    Authorization: `Bearer ${token}`,
  },
  body: JSON.stringify({
    text: text,
    mic_on: false,
    camera_on: false,
  }),
});


