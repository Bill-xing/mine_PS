%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% SPDX-License-Identifier: BSD-3-Clause
% Copyright (c) 2020, Salman Ahmad Faris
% https://github.com/salfaris/EasyPS
% Copyright (c) 2024, Daize Dong
% https://github.com/DaizeDong/Easier-PS-and-SoP
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{easier_ps}[2024/10/21 Modified from EasyPS]
\LoadClass[12pt]{article} % Load the base article class with 12pt font size
\RequirePackage{iftex}
\ifPDFTeX
  \pdfgentounicode=1  % Ensure generated PDF is ATS parsable
\fi

\RequirePackage{lipsum}         % Generates placeholder text, remove if unnecessary
\RequirePackage{geometry}       % For layout and margin control
\RequirePackage{fancyhdr}       % For headers and footers
\RequirePackage{setspace}       % For controlling line spacing
\RequirePackage{titlesec}       % For section title formatting
\RequirePackage{lmodern}        % Load LM Roman (Latin Modern Roman)

% BASIC INFO
\def\@StudentName{Student Name Here}
\newcommand*{\SetStudentName}[1]{\def\@StudentName{#1}}
\newcommand*{\GetStudentName}{\@StudentName}
\def\@ProgramName{Program Name Here}
\newcommand*{\SetProgramName}[1]{\def\@ProgramName{#1}}
\newcommand*{\GetProgramName}{\@ProgramName}
\def\@UniversityName{University Name Here}
\newcommand*{\SetUniversityName}[1]{\def\@UniversityName{#1}}
\newcommand*{\GetUniversityName}{\@UniversityName}
\def\@UniversityAbbr{\@UniversityName}
\newcommand*{\SetUniversityAbbr}[1]{\def\@UniversityAbbr{#1}}
\newcommand*{\GetUniversityAbbr}{\@UniversityAbbr}

% CONTENTS INFO
\def\@BaseContentPath{main/content/base}
\newcommand*{\SetBaseContentPath}[1]{\def\@BaseContentPath{#1}}
\newcommand*{\GetBaseContentPath}{\@BaseContentPath}
\def\@UniContentPath{main/content/base}
\newcommand*{\SetUniContentPath}[1]{\def\@UniContentPath{#1}}
\newcommand*{\GetUniContentPath}{\@UniContentPath}

% LAYOUT SETTINGS
\geometry{a4paper, includehead, includefoot, left=1.0in, right=1.0in, top=0.4in, bottom=0.4in} % Include header/footer in layout
\setlength{\parskip}{0.2em}     % Space between paragraphs
\linespread{1.06}               % Line spacing

% HEADER AND FOOTER SETTINGS
\pagestyle{fancy}               % Use fancy headers/footers
\fancyhf{}                      % Clear default header/footer
\fancyhead[L]{\@StudentName}    % Custom left header: Student Name
\fancyhead[R]{\@UniversityAbbr} % Keep continuation headers compact and non-overlapping
\fancyfoot[C]{\thepage}         % Add a page number in the footer
\setlength{\headheight}{53pt}   % Adjust the height of the header
\setlength{\headsep}{16pt}      % Space between the header and content
\setlength{\footskip}{18pt}     % Ensure footer is separated from text

% HEADER EXPANSION FOR FIRST PAGE
\fancypagestyle{firstpageheader}{
    \fancyhf{} % Clear header and footer for first page
    \fancyhead[C]{%
        \parbox[b]{\textwidth}{%
            \centering
            {\LARGE \textsc{Personal Statement}}\\[0.35em]% Title line
            \makebox[\textwidth][r]{\@UniversityName}\\% University Name on the right
            \makebox[\textwidth][l]{\@StudentName \hfill \@ProgramName}% Student and Program aligned
        }%
    }
    \fancyfoot[C]{\thepage}       % Add a page number in the footer
}
