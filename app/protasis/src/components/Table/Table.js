import React from 'react';
import { DataGrid } from '@mui/x-data-grid';


class Table extends React.Component
{

    

    /**
     * Formats columns in a MUI/DataGrid supported way.
     * @param {*} columns   The columns.
     * @returns             Formatted columns.
     */
    formatColumns(columns){
        var c = [];
        /**
         * Format columns
         */
         if(columns){
            columns.forEach(element => {
               c.push({ field: element, headerName: element, flex: 0.3});    
            });
            return c;
        }
        return null;
    }

    /**
     * Formats rows in a MUI/DataGrid supported way.
     * @param {*} rows  The rows
     * @returns         Formatted rows.
     */
    formatRows(rows){
        var r = [];

        if(rows){
            var rowCount = 0;
            rows.forEach(element => {
                rowCount++;
                Object.assign(element, {"id": rowCount})
                r.push(element);
            });
            
            return r;
        }
        return null;
    }

    render()
    {
        
        
        /**
         * Decompose params, format rows,columns in a supported by mui way.
         */
        const {columns, rows, userSelectionHandler} = this.props;
        const r = this.formatRows(rows);
        const c = this.formatColumns(columns);
       
        
        
        /**
         * Return a DataGrid filled with data, or just an empty div.
         */
        return(  <div style={{ height: 500, width: '60%' }}>
                    {(r && c) ? 
                    <DataGrid               
                                            
                                            rows={r} 
                                            columns={c} 
                                            columnVisibilityModel={{
                                                // Hide the id collumn from view.
                                                id: false
                                            }}
                                            getRowId={(row) => row.id}
                                            onRowClick={(e) => { userSelectionHandler(e) }}
                                            sx={
                                                {
                                                 '& .MuiDataGrid-main':{
                                                     boxShadow: 'rgba(0, 0, 0, 0.25) 0px 54px 55px, rgba(0, 0, 0, 0.12) 0px -12px 30px, rgba(0, 0, 0, 0.12) 0px 4px 6px, rgba(0, 0, 0, 0.17) 0px 12px 13px, rgba(0, 0, 0, 0.09) 0px -3px 5px;'
                                                 },   
                                                 '& .MuiDataGrid-columnHeaders':{
                                                    backgroundImage: 'linear-gradient(to right, #ff9966, #ff5e62)',
                                                    borderRadius: '6px',
                                                    color: '#f5f5f5'
                                                },   
                                                '& .MuiDataGrid-row:hover':{
                                                    backgroundImage: 'linear-gradient(to right, #ff9966, #ff5e62)',
                                                    color: '#f5f5f5'
                                                },
                                                '& .MuiDataGrid-row:focus':{
                                                    backgroundImage: 'linear-gradient(to right, #ff9966, #ff5e62)',
                                                    color: '#f5f5f5'
                                                },
                                                '& .MuiDataGrid-row.Mui-selected':{
                                                    backgroundImage: 'linear-gradient(to right, #ff9966, #ff5e62)',
                                                },
                                                '& .MuiDataGrid-cell:focus':{
                                                    outline:'solid transparent 1px' 
                                                },
                                                '& .MuiDataGrid-footerContainer':{
                                                    backgroundImage: 'linear-gradient(to right, #ff9966, #ff5e62)',
                                                    borderRadius: '6px',
                                                    color: '#f5f5f5'
                                                },
                                                '& .MuiToolbar-root':{
                                                    borderRadius: '6px',
                                                    color: '#f5f5f5'
                                                }
                                        }
                                        }
                                            
                    /> 
                    : null}
                </div>
        );
    }

}

export default Table;