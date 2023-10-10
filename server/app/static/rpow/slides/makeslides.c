/* Output slides for RPOW presentation */
#include <stdio.h>

char *template =
"<html>\n"
"<head>\n"
"<title>Slide %d</title>\n"
"</head>\n"
"<body>\n"
"<table width=\"100%\"><tr align=\"center\">\n"
"<font size=\"+1\">\n"
"<td width=\"20%\"><a href=\"slide%03d.html\"><img src=\"ltarrow.gif\"></a></td>\n"
"<td width=\"60%\"><a href=\"../index.html\"><img src=\"uparrow.gif\"></a></td>\n"
"<td width=\"20%\"><a href=\"slide%03d.html\"><img src=\"rtarrow.gif\"></a></td>\n"
"</font>\n"
"</tr>\n"
"<tr align=\"center\">\n"
"<td colspan=\"3\">\n"
"<br>\n"
"<img src=\"%s\">\n"
"</td></tr></table>\n"
"</body>\n"
"</html>\n";

/* Pass file with the necessary files, in order */
main(int ac, char **av)
{
	char buf[1000];
	char buf1[1000];
	char filename[1000];
	int slidenum = 1;
	int prevnum;
	int nextnum;
	int last = 0;
	FILE *f;

	fgets (buf, sizeof(buf), stdin);

	do
	{
		buf[strlen(buf)-1] = '\0';
		last = fgets (buf1, sizeof(buf1), stdin) == NULL;
		prevnum = (slidenum == 1) ? 1 : slidenum-1;
		nextnum = last ? slidenum : slidenum+1;
		sprintf (filename, "slide%03d.html", slidenum);
		f = fopen(filename, "w");
		fprintf (f, template, slidenum, prevnum, nextnum, buf);
		fclose (f);
		strcpy (buf, buf1);
		++slidenum;
	} while (!last);
}
