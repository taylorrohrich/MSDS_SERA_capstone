import "../App.css"
const Table = (props)=>{
    const {rows,columns} = props
    console.log(rows,columns)
    return  <div style={{display: "flex",flexDirection:'column',marginLeft: 20,marginRight: 20}}>
                <div style={{margin:20,fontSize:32}}>Participant Tracker</div>
                <table style={{flex:1}}> 
                    <TableRow data={columns} type={'header'}/>
                    {rows.map(row=> <TableRow data={row}/>)}
                </table>
            </div>
}

const TableRow = ({data,type})=>{
    console.log(data,type)
    return <tr className={type=="header" ? 'table-header-row' : null}>
        {data.map(item=>type === "header" ? <th style={{padding:10}}>{item}</th> : <td>{item}</td>)}
    </tr>
}

export default Table