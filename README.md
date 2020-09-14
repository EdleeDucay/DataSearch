General input format:<br/>
expression						 ::=	dateQuery	|	priceQuery	|	scoreQuery	|	termQuery	<br/>
query											 ::=	expression	(whitespace	expression)?<br/>
modeChange ::=	'output=full'	|	'output=brief'<br/>
command ::=	query	|	modeChange<br/>
dateQuery					 ::=	‘date’ +	(	'>'	|	'<')+	YYYY/MM/DD<br/>
priceQuery ::=	(price)	+	(	'>'	|	'<') +	numeric<br/>
scoreQuery ::=	(score)	+	(	'>'	|	'<') +	numeric<br/>
termPrefix ::=	(pterm	|	rterm)	+ ':'<br/>
termSuffix						 ::=	'%'	<br/>
termQuery							 ::=	termPrefix?	+ term	termSuffix?<br/>
