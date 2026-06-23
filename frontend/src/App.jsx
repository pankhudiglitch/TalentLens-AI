import { useEffect, useState } from "react"
import "./App.css"

export default function App(){

const [candidates,setCandidates]=useState([])
const [loading,setLoading]=useState(true)

useEffect(()=>{

async function load(){

try{

const res=
await fetch(
"http://127.0.0.1:8000/shortlist"
)

const data=
await res.json()

console.log(data)

setCandidates(
data.top_candidates || []
)

}
catch(err){

console.log(err)

}
finally{

setLoading(false)

}

}

load()

},[])

return(

<div className="app">

<h3>AI Talent Intelligence</h3>

<h1>TalentLens AI</h1>

<p>Find Top Candidates Ranked By AI</p>

{

loading ?

<h2>Loading...</h2>

:

<div className="cards">

{

candidates.map((c,index)=>(

<div
className="card"
key={c.candidate_id}
>

<div>

#{index+1}

</div>

<h2>

{c.name}

</h2>

<p>

{c.headline}

</p>

<div>

⭐ {c.score}

</div>

<div>

⏳ {c.experience} years

</div>

</div>

))

}

</div>

}

</div>

)

}