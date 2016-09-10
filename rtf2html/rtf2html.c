/*RTF2HTML.c, Chuck Shotton - 6/21/93 */
/************************************************************************
 * This program takes a stab at converting RTF (Rich Text Format) files
 * into HTML. There are some limitations that keep RTF from being able to
 * easily represent things like in-line images and anchors as styles. In
 * particular, RTF styles apply to entire "paragraphs", so anchors or
 * images in the middle of a text stream can't easily be represented by
 * styles. The intent is to ultimately use something like embedded text
 * color changes to represent these constructs. 
 * 
 * In the meantime, you can take existing Word documents, apply the
 * correct style sheet, and convert them to HTML with this tool.
 *
 * AUTHOR: Chuck Shotton, UT-Houston Academic Computing,
 *         cshotton@oac.hsc.uth.tmc.edu
 *
 * USAGE: rtf2html [rtf_filename] 
 *
 * BEHAVIOR:
 *        rtf2html will open the specified RTF input file or read from
 *        standard input, writing converted HTML to standard output.
 *
 * NOTES:
 *        The RTF document must be formatted with a style sheet that has
 *        style numberings that conform to the style_mappings table
 *        defined in this source file.
 *
 * MODIFICATIONS:
 *        6/21/93 : Chuck Shotton - created version 1.0.
 *
 ************************************************************************/

/* Note, the source is formated with 4 character tabs */

#include <stdio.h>
#include <string.h>

#ifdef THINK_C
#include <console.h>
#endif

#ifndef TRUE
#define TRUE -1
#define FALSE 0
#endif

#define MAX_LEVELS 20	/*defines the # of nested in-line styles (pairs of {})*/
#define MAX_STYLES 12
#define MAX_INLINE_STYLES 4 /*defines # of in-line styles, bold, italic, etc.*/

typedef enum {s_plain, s_bold, s_italic, s_underline, /*in-line styles*/
		s_para,		  /*pseudo style*/
		s_h0, s_h1, s_h2, s_h3, s_h4, s_h5, s_h6 /*heading styles*/
} StyleState;

char *styles[MAX_STYLES][2] = {		/*HTML Start and end tags for styles*/
	{"", ""},
	{"<b>", "</b>"},
	{"<i>", "</i>"},
	{"<em>", "</em>"},
	{"<p>", ""},
	{"", ""},
	{"<h1>", "</h1>"},
	{"<h2>", "</h2>"},
	{"<h3>", "</h3>"},
	{"<h4>", "</h4>"},
	{"<h5>", "</h5>"},
	{"<h6>", "</h6>"}
};

/* style_mappings maps the style numbers in a RTF style sheet into one of the*/
/* (currently) six paragraph-oriented HTML styles (i.e. heading 1 through 6.)*/
/* Additional styles for lists, etc. should be added here. Style info        */
/* ultimately should be read from some sort of config file into these tables.*/

char *style_mappings[7] = {
	"", "255", "254", "253", "252", "251", "250"
};

/* RTF tokens that mean something to the parser. All others are ignored. */

typedef enum {t_start,t_fonttbl, t_colortbl, t_stylesheet, t_info,
			t_s, t_b, t_u, t_i, t_plain, t_par, t_end} TokenIndex;

char *tokens[] = {
	"###",
	"fonttbl",
	"colortbl",
	"stylesheet",
	"info",
	"s",
	"b",
	"ul",
	"i",
	"plain",
	"par",
	"###"
};

char style_state[MAX_LEVELS][MAX_INLINE_STYLES], curr_style[MAX_INLINE_STYLES];
short curr_heading;

short 	level,		/*current {} nesting level*/ 
	skip_to_level,/*{} level to which parsing should skip (used to skip */ 
	              /*  font tables, style sheets, color tables, etc.)    */ 
	gobble,	/*Flag set to indicate all input should be discarded  */ 
	ignore_styles;/*Set to ignore inline style expansions after style use*/

/**************************************/

char RTF_GetChar(f)
FILE *f;
{
	return fgetc(f);
}

/**************************************/

void RTF_PutStr(s)
char *s;
{
	if (gobble) return;
	fputs(s, stdout);
}

/**************************************/

void RTF_PutChar(ch)
char ch;
{
	if (gobble) return;
	switch (ch) {
		case '<':
			RTF_PutStr("&lt");
			break;
			
		case '>':
			RTF_PutStr("&gt");
			break;
			
		case '&':
			RTF_PutStr("&amp");
			break;
		
		default:
			fputc(ch, stdout);
	}
}


/**************************************/

void RTF_PlainStyle (s)
char *s;
{
int j;
	for (j=0;j<MAX_INLINE_STYLES;j++)
		s[j] = (char) 0;
}

/**************************************/

void RTF_CopyStyle (s, d)
char *s, *d;
{
int j;
	for (j=0;j<MAX_INLINE_STYLES;j++)
		d[j] = s[j];
}

/**************************************/

void RTF_PushState(level)
short *level;
{
	RTF_CopyStyle (curr_style, style_state[*level]);
	(*level)++;
}

/**************************************/

void RTF_PopState(level)
short *level;
{
int j;
	/*close off any in-line styles*/
	for (j=0;j<MAX_INLINE_STYLES;j++) {
		if (curr_style[j])
			RTF_PutStr(styles[j][1]);
	}
	
	(*level)--;
	RTF_CopyStyle (style_state[*level], curr_style);

	if (*level == skip_to_level) {
		skip_to_level = -1;
		gobble = FALSE;
	}
}

/**************************************/

void RTF_Title(s)
char *s;
{
	fprintf (stdout, "<title>%s</title>", s);
}

/**************************************/

void RTF_BuildToken (token, ch)
char *token;
char ch;
{
	strncat (token, &ch, 1);
}

/**************************************/
/* Map a style number into a HTML heading */

short RTF_MapStyle(s)
char *s;
{
int i;
	for (i=0;i<7;i++)
		if (!strcmp(style_mappings[i], s))
			return (i);
	return (0);
}

/**************************************/
/* Perform actions for RTF control words */

void RTF_DoControl (control, arg)
char *control, *arg;
{
TokenIndex i;
short style;

	if (gobble) return;

	for (i=t_start; i<t_end; i++) {
		if (!strcmp(control, tokens[i]))
			break;
	}
	
	switch (i) {
		case t_fonttbl:	/*skip all of these and their contents!*/
		case t_colortbl:
		case t_stylesheet:
		case t_info:
			gobble = TRUE;	/*perform no output, ignore commands 'til level-1*/
			skip_to_level = level-1;
			break;
			
		case t_s: /*Style*/
			style = RTF_MapStyle (arg);
			curr_heading = s_h0 + style;
			RTF_PutStr(styles[curr_heading][0]);
			ignore_styles = TRUE;
			break;
			
		case t_b: /*Bold*/
			if (!ignore_styles) {
				RTF_PutStr(styles[s_bold][0]);
				curr_style[s_bold] = TRUE;
			}
			break;
			
		case t_u: /*Underline, maps to "emphasis" HTML style*/
			if (!ignore_styles) {
				RTF_PutStr(styles[s_underline][0]);
				curr_style[s_underline] = TRUE;
			}
			break;
			
		case t_i: /*Italic*/
			if (!ignore_styles) {
				RTF_PutStr(styles[s_italic][0]);
				curr_style[s_italic] = TRUE;
			}
			break;
			
		case t_par: /*Paragraph*/
			if (curr_heading) {
				RTF_PutStr(styles[curr_heading][1]);
				curr_heading = s_plain;
			}
			else {
				RTF_PutStr(styles[s_para][0]);
			}
			ignore_styles = FALSE;
			break;
			
		case t_plain: /*reset inline styles*/
			RTF_PlainStyle(curr_style);
			break;
	}
			
}

/**************************************/
/* RTF_Parse is a crude, ugly state machine that understands enough of */
/* the RTF syntax to be dangerous.                                     */

typedef enum {plaintext, control, argument, backslash} ParseState;

int RTF_Parse (filename)
char *filename;
{
FILE *f;
char ch;
ParseState state;
char token[40], arg[40];

	if (filename) {
		if (!(f = fopen (filename, "r"))) {
			fprintf (stderr, "\nError: Input file %s not found.\n", filename);
			return (-1);
		}
		RTF_Title(filename);
	}
	else {
		f = stdin;
		RTF_Title("STDIN");
	}
		
	state = plaintext;
	level = 0;
	skip_to_level = -1;
	gobble = FALSE;
	ignore_styles = FALSE;
	
	while (!feof(f)) {
		/*get a character*/
		ch = RTF_GetChar(f);
		
		switch (state) {
		
			case plaintext: /*this is just normal user content*/
				switch (ch) {
					case '\\':
						state = backslash;
						break;
					
					case '{':
						RTF_PushState(&level);
						break;
					
					case '}':
						RTF_PopState(&level);
						break;
						
					default:
						RTF_PutChar(ch);
						break;
				}
				break;
				
			case backslash: /*something special like a command or escape*/
				switch (ch) {
					case '\\':
					case '{':
					case '}':
						RTF_PutChar(ch);
						state = plaintext;
						break;
						
					default:
						if (isalpha(ch)) {
							state = control;
							token[0]='\0';
							RTF_BuildToken(token, ch);
						}
						else {
							fprintf(stderr, "\nRTF Error: unexpected '%c' after \\.\n", ch);
						}
						break;
				}
				break;
				
			case control: /*collecting the command token*/
				if (isalpha(ch)) {
					RTF_BuildToken(token, ch);
				}
				else if (isdigit(ch)) {
					state = argument;
					arg[0]='\0';
					RTF_BuildToken(arg, ch);
				}
				else {
					RTF_DoControl (token, "");
					state = plaintext;
					
					switch (ch) {
						case '\\':
							state = backslash;
							break;

						case '{':
							RTF_PushState(&level);
							break;
						
						case '}':
							RTF_PopState(&level);
							break;
						
						default:
							if (!isspace(ch)) RTF_PutChar(ch);
							break;
					}
				}
				break;
				
			case argument: /*collecting the optional command argument*/
				if (isdigit(ch)) {
					RTF_BuildToken(arg, ch);
				}
				else {
					state = plaintext;
					RTF_DoControl (token, arg);
					switch (ch) {
						case '\\':
							state = backslash;
							break;

						case '{':
							RTF_PushState(&level);
							break;
						
						case '}':
							RTF_PopState(&level);
							break;
						
						default:
							if (!isspace(ch)) RTF_PutChar(ch);
							break;
					}
				}
				break;
		}/*switch*/
	}/*while*/
	
	fclose (f);
}

/**************************************/

void Initialize()
{
int i,j;

	for (i=0;i<MAX_LEVELS;i++)
		for (j=0;j<MAX_STYLES;j++)
			RTF_PlainStyle(style_state[i]);

	RTF_PlainStyle(curr_style);
	curr_heading = s_plain;
}

/**************************************/

main(argc, argv)
int argc;
char **argv;
{
#ifdef THINK_C
	argc = ccommand (&argv);
#endif

	Initialize();
	
	if (argc>1)
		return (RTF_Parse(argv[1]));
	else
		return (RTF_Parse(NULL));
}
