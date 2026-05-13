      ******************************************************************
      * FEE_CALC.cob — Legacy Bank Fee Calculator
      * System  : COBOL/Z  IBM Banking Legacy Core
      * Compiler: GnuCOBOL 3.x  (cobc -x -o fee_calc FEE_CALC.cob)
      *
      * Input  (stdin) : line 1 = amount (numeric, e.g. 500.00)
      *                  line 2 = transaction type string
      * Output (stdout): fee as decimal string (e.g. 12.80)
      *
      * Fee schedule (unchanged since 2009 contract):
      *   domestic      : 2.5% + $0.30 flat
      *   international : 2.5% + $0.30 flat + 2.0% FX margin
      *   instant       : 0.5% + $0.50 flat
      *   wire_transfer : 0.15% + $15.00 flat (SWIFT legacy pricing)
      *   default       : 2.5% + $0.30 flat
      *
      * Rounding: ROUNDED (half-down per COBOL default on IBM z/OS)
      ******************************************************************
       IDENTIFICATION DIVISION.
       PROGRAM-ID. FEE-CALC.
       AUTHOR. IBM-LEGACY-BANKING-CORE.
       DATE-WRITTEN. 2009-03-15.
       DATE-COMPILED.

       ENVIRONMENT DIVISION.
       CONFIGURATION SECTION.
       SOURCE-COMPUTER. IBM-Z15.
       OBJECT-COMPUTER. IBM-Z15.

       DATA DIVISION.
       WORKING-STORAGE SECTION.
       01 WS-AMOUNT-STR       PIC X(24)  VALUE SPACES.
       01 WS-TXN-TYPE         PIC X(24)  VALUE SPACES.
       01 WS-AMOUNT           PIC 9(12)V99 VALUE ZEROS.
       01 WS-FEE              PIC 9(12)V99 VALUE ZEROS.
       01 WS-BASE-FEE         PIC 9(12)V99 VALUE ZEROS.
       01 WS-FX-MARGIN        PIC 9(10)V9(6) VALUE ZEROS.
       01 WS-FEE-OUT          PIC Z(10)9.99 VALUE ZEROS.
       01 WS-TRIMMED          PIC X(14)  VALUE SPACES.

       PROCEDURE DIVISION.
       MAIN-PARA.
           ACCEPT WS-AMOUNT-STR
           ACCEPT WS-TXN-TYPE

           MOVE FUNCTION NUMVAL(WS-AMOUNT-STR) TO WS-AMOUNT

           EVALUATE FUNCTION TRIM(WS-TXN-TYPE, TRAILING)
               WHEN "domestic"
                   COMPUTE WS-FEE ROUNDED =
                       WS-AMOUNT * 0.025 + 0.30

               WHEN "international"
                   COMPUTE WS-BASE-FEE ROUNDED =
                       WS-AMOUNT * 0.025 + 0.30
                   COMPUTE WS-FX-MARGIN ROUNDED =
                       WS-AMOUNT * 0.020
                   COMPUTE WS-FEE ROUNDED =
                       WS-BASE-FEE + WS-FX-MARGIN

               WHEN "instant"
                   COMPUTE WS-FEE ROUNDED =
                       WS-AMOUNT * 0.005 + 0.50

               WHEN "wire_transfer"
                   COMPUTE WS-FEE ROUNDED =
                       WS-AMOUNT * 0.0015 + 15.00

               WHEN OTHER
                   COMPUTE WS-FEE ROUNDED =
                       WS-AMOUNT * 0.025 + 0.30
           END-EVALUATE

           MOVE WS-FEE TO WS-FEE-OUT
           MOVE FUNCTION TRIM(WS-FEE-OUT, LEADING) TO WS-TRIMMED
           DISPLAY FUNCTION TRIM(WS-TRIMMED, TRAILING)

           STOP RUN.
