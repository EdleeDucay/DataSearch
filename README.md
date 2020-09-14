# DataSearch
Information retrieval system that utilizes the Berkeley DB library for operations

General input format:
expression						 ::=	dateQuery	|	priceQuery	|	scoreQuery	|	termQuery	
query											 ::=	expression	(whitespace	expression)?
modeChange ::=	'output=full'	|	'output=brief'
command ::=	query	|	modeChange
dateQuery					 ::=	‘date’ +	(	'>'	|	'<')+	YYYY/MM/DD
priceQuery ::=	(price)	+	(	'>'	|	'<') +	numeric
scoreQuery ::=	(score)	+	(	'>'	|	'<') +	numeric
termPrefix ::=	(pterm	|	rterm)	+ ':'
termSuffix						 ::=	'%'	
termQuery							 ::=	termPrefix?	+ term	termSuffix?
