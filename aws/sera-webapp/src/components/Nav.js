
import {Link } from "react-router-dom";

const navList = [{
    to:"/",
    text:'Tracker'
},
{
    to:"query",
    text:'Query'
}]
const Nav = (props)=>{
    return <div style={{display:"flex",flexDirection:"row",justifyContent:'flex-start',alignItems:'center',backgroundColor:'#232D4B'}}>
        {navList.map(item=><NavItem text={item.text} to={item.to}/>)}
    </div>
}

export default Nav

const NavItem = (props)=>{
    return <Link to={props.to} style={{margin:'15px',color:"white",fontWeight:"bold"}}>
        {props.text}
    </Link>
}