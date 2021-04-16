import "../App.css"
import { useState } from "react"
import { CSVLink, CSVDownload } from "react-csv";
const Table = (props)=>{
    const {rows,columns} = props
    const [searchId, setSearchId] = useState('')
    const filteredRows = searchId.length ? rows?.filter(row=>row?.[0].includes(searchId)) : rows
    // console.log(rows,columns)
    return  <div style={{display: "flex",flexDirection:'column',marginLeft: 20,marginRight: 20}}>
                <div style={{margin:20,fontSize:32}}>Participant Tracker</div>
                <div style={{display:"flex", flexDirection:'row',marginLeft: 20,marginBottom: 20}}>
                <input style={{marginRight: 20}} placeholder='Search by ID' value={searchId} onChange={e=>setSearchId(e.target.value)}></input>
                <CSVLink style={{color:'#232D4B'}} data={[columns,...filteredRows]} filename={"participant_tracker.csv"}>Download </CSVLink>
                </div>
                <table style={{flex:1}}> 
                    <TableRow data={columns} type={'header'}/>
                    {filteredRows.map(row=> <TableRow data={row}/>)}
                </table>
            </div>
}

const TableRow = ({data,type})=>{
    return <tr className={type=="header" ? 'table-header-row' : null}>
        {data.map(item=>type === "header" ? <th style={{padding:10}}>{item}</th> : <td>{item}</td>)}
    </tr>
}

export default Table