# single price specified
EX_SP_1 = ("£34866 P.A.", "34866")
EX_SP_2 = ("£48260 P.A.", "48260")
EX_SP_3 = ("60000.00", "60000")
EX_SP_4 = ("60K", "60000")
EX_SP_5 = ("45000", "45000")
EX_SP_6 = ("£60K", "60000")
"£42983 P.A."
"£46129 P.A."
"£38580 P.A."
"£42983 P.A."
"£49513 P.A."
EX_SP_7 = ("45000 + BONUS", "45000")
"65000 + BONUS + EQUITY"
# spot contiguous number, strip currency symbol

# range annual salary (compounds)
EX_CP_1 = ("30K - 50K PA", "30000,50000")
EX_CP_2 = ("40K - 70K PA + BENEFITS", "40000,70000")
EX_CP_3 = ("FROM 40000 TO 70000 PER ANNUM", "40000,70000")
"50000 - 55000 PER ANNUM + BONUS + EXCELLENT BENEFITS"
"30000 - 40000"
"35K - 45K PA"
"50K.00 - 65K PA"
"40K - 70K PA + BENEFITS"
"35000 - 45000 PER ANNUM + BENEFITS"
"50K - 70K PA"
"32000 - 42000 PER ANNUM PLUS BONUS & BENEFITS"
"60000.00 - 80000.00 PER ANNUM + BONUS HEALTHCAR…"
"40000 - 60000 PER ANNUM"
"40000 - 65000 PER ANNUM + BENEFITS"
"60K - 70K PA + BENEFITS"
"35K TO 45K + BONUS + BENEFITS"
# spot contiguous numbers with a separator (normalise - TO to a range_separator
# symbol?), expand K->000
# it would be nice to return attributes e.g. per annum, gbp etc

# range day rate
"350 - 450 P DAY"


# upper limit ?
"UP TO 37000 + BONUS (UP TO 50%) + BENEFITS"
"UP TO 37000 + BONUS (UP TO 50%) + BENEFITS"
"UP TO 37000 + BONUS (UP TO 50%) + BENEFITS"
"TO 65K + BENEFITS"

# price unspecified
"COMPETITIVE - RANGE OF LEVELS"
"COMPETITIVE"
"MARKET LEADING"


# poor formatting
"30 - 50000 + BONUS + BENEFITS"


# what about examples for prices e.g. £23.99 or $1.23USD ?
