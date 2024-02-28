from data_processing.dataProcessing import column_sum, no_data_modules
from data_processing.dataframeCleaning import df_requestedVsRecruitedCleaned, df_capVsActualStudentsCleaned
from dash import html, dcc

# list modules with 'no data found' in their respective years
noDataModules2122 = no_data_modules(df_requestedVsRecruitedCleaned, '2021-22 requested', '2021-22 recruited')
noDataModules2223 = no_data_modules(df_requestedVsRecruitedCleaned, '2022-23 requested', '2022-23 recruited')
noDataModules2324 = no_data_modules(df_requestedVsRecruitedCleaned, '2023-24 requested', '2023-24 recruited')


stats_layout = html.Div([
    html.Div([
        dcc.Markdown("**Total PGTAs Recruited in 21-22:** " + str(column_sum(df_requestedVsRecruitedCleaned, '2021-22 recruited'))),
        dcc.Markdown("**Total PGTAs Recruited in 22-23:** " + str(column_sum(df_requestedVsRecruitedCleaned, '2022-23 recruited'))),
        dcc.Markdown("**Total PGTAs Recruited in 23-24:** " + str(column_sum(df_requestedVsRecruitedCleaned, '2023-24 recruited'))),
    ], className='stats-column'),
    html.Div([
        dcc.Markdown("**Total PGTAs Requested in 21-22:** " + str(column_sum(df_requestedVsRecruitedCleaned, '2021-22 requested'))),
        dcc.Markdown("**Total PGTAs Requested in 22-23:** " + str(column_sum(df_requestedVsRecruitedCleaned, '2022-23 requested'))),
        dcc.Markdown("**Total PGTAs Requested in 23-24:** " + str(column_sum(df_requestedVsRecruitedCleaned, '2023-24 requested'))),
    ], className='stats-column'),
    html.Div([
        dcc.Markdown("**Total Students in 22-23:** " + str(column_sum(df_capVsActualStudentsCleaned, '2022-23 actual students')))
    ])
], className='stats-container')
