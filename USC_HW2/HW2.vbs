Sub abc():

'For loop that runs through all the sheets
For Each ws In Worksheets
    Dim WorksheetName As String
    WorksheetName = ws.Name
    ActiveWorkbook.Sheets(WorksheetName).Activate
    
   'Setting the title of each column
    Cells(1, 9).Value = "Ticker"
    Cells(1, 10).Value = "Yearly Change"
    Cells(1, 11).Value = "Percent Change"
    Cells(1, 12).Value = "Total Stock Volume"
    Range("P1").Value = "Ticker"
    Range("Q1").Value = "Value"
    Range("O2").Value = "Greatest % Increase"
    Range("O3").Value = "Greatest % Decrease"
    Range("O4").Value = "Greatest Total Volume"
    
    'Set an initial variable for holding the stock name
    Dim Stock_Name As String
    
    'Set an initial variable for holding the total per stock brand
    Dim Stock_Total As Double
    Stock_Total = 0

    'Keep track of the location for each stock brand in the summary table
    Dim Stock_Table_Row As Long
    Stock_Table_Row = 2
      
    'Set an initial variable for holding the open value of a stock brand
    Dim New_open As Double
    New_open = Cells(2, 3).Value
        
    'Defining Percentage change variable
    Dim Percentage_change As Double
    
   '---------------------------------------------------------------------------------------------
    'Second for loop that runs through all the row of each sheet
     For I = 2 To 800001
    
        'Check if we are still within the same stock brand, if it is not...
        If Cells(I + 1, 1).Value <> Cells(I, 1).Value Then
    
              'Set the Stock name
              Stock_Name = Cells(I, 1).Value
        
              'Add to the Stock Total
              Stock_Total = Stock_Total + Cells(I, 7).Value
              
              'Yearly change from opening price at the beginning of a given year to the closing price at the end of that year
              Yearly_Change = Cells(I, 6).Value - New_open
              
              'Print the Stock Brand in the Summary Table
              Range("I" & Stock_Table_Row).Value = Stock_Name
              
              'Print the Yearly change to the Summary Table
              Range("J" & Stock_Table_Row).Value = Yearly_Change
              
              ' ----------Statement that sets the colors for cell values---------
                If Range("J" & Stock_Table_Row).Value < 0 Then
                   Range("J" & Stock_Table_Row).Interior.ColorIndex = 3 'Red
                Else
                     Range("J" & Stock_Table_Row).Interior.ColorIndex = 4 'Green
                End If
            
              '---------Prints the Percentage Change----------------------
              'If Statement that checks if the initial value of a stock is zero
              If New_open <> 0 Then
                Percentage_change = (Cells(I, 6).Value - New_open) / New_open
                Range("K" & Stock_Table_Row).Value = Percentage_change
              Else
                Percentage_change = 0.1
                Range("K" & Stock_Table_Row).Value = Percentage_change
                
              End If
        
              'Print the Stock Amount to the Summary Table
              Range("L" & Stock_Table_Row).Value = Stock_Total
        
              'Add one to the summary table row
              Stock_Table_Row = Stock_Table_Row + 1
            
              'Reset the Stock Total
              Stock_Total = 0
              
              'Updates the value of new open volume for new stock
              New_open = Cells(I + 1, 3).Value
              
            Else
              ' Add to the Stock Total
              Stock_Total = Stock_Total + Cells(I, 7).Value
        End If
    Next I
    
   '---------------------------------------------------------------------------------------------
    'Sets the intial value of the Greatest Percentage Increase and Ticker for that value
    Greatest = 0
    Ticker = Cells(2, 1).Value
    
    'lastrow takes number of the last row
    lastrow = Cells(Rows.Count, 1).End(xlUp).Row
    
    'Third for loop finds the Greatest % Increase
    For j = 2 To lastrow
       'If statement that checks if the current cell is greater than the value of Greatest
        If Cells(j, 11).Value > Greatest Then
            Greatest = Cells(j, 11).Value
            Ticker = Cells(j, 9).Value
            
            'Prints the value of the Greatest value and the Ticker
            Range("P2").Value = Ticker
            Range("Q2").Value = Greatest
        End If
    Next j
     
   '---------------------------------------------------------------------------------------------
    'Sets the initial value of the Greatest Percentage Decrease
    Greatest1 = 0
    
    'Fourth for loop runs find the Greatest Percentage Decrease
    For h = 2 To lastrow
       'If statement that checks if the current value is less than the Greatest current value
        If Cells(h, 11).Value < Greatest1 Then
            Greatest1 = Cells(h, 11).Value
            Ticker = Cells(h, 9).Value
            
            'Prints the value of the Greatest Percentage Decrease value and the Ticker
            Range("P3").Value = Ticker
            Range("Q3").Value = Greatest1
        End If
    Next h
    
   '---------------------------------------------------------------------------------------------

    'Sets the intial value of the Greatest Percentage Increase
    Greatest2 = 0
    
    'lastrow takes number of the last row
    lastrow = Cells(Rows.Count, 1).End(xlUp).Row
    
    'Fifth for loop finds the Greatest % Increase
    For k = 2 To lastrow
       'If statement that checks if the current cell is greater than the value of Greatest
        If Cells(k, 12).Value > Greatest2 Then
            Greatest2 = Cells(k, 12).Value
            Ticker = Cells(k, 9).Value
            
            'Prints the value of the Greatest value and the Ticker
            Range("P4").Value = Ticker
            Range("Q4").Value = Greatest2
        End If
    Next k


Next

End Sub


