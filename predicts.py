from scipy.stats import poisson,skellam
from prettytable import PrettyTable

def predict_outcome(home,away,opt):
	if opt is "scored":
		[H,D,A] = predict_outcome_part_scored(home, away,0)
		[H_1,D_1,A_1] = predict_outcome_part_scored(home, away,1)
		[H_2,D_2,A_2] = predict_outcome_part_scored(home, away,2)
	else:
		[A,D,H] = predict_outcome_part_conceded(home, away,0)
		[A_1,D_1,H_1] = predict_outcome_part_conceded(home, away,1)
		[A_2,D_2,H_2] = predict_outcome_part_conceded(home, away,2)

	print_result(home,away,[H,D,A,H_1,D_1,A_1,H_2,D_2,A_2])

def predict_outcome_part_scored(home, away, n):
	if n==1:
		H = skellam.pmf(1,home.hScored_first,away.aScored_first)+skellam.pmf(2,home.hScored_first,away.aScored_first)+skellam.pmf(3,home.hScored_first,away.aScored_first)+skellam.pmf(4,home.hScored_first,away.aScored_first)
		D = skellam.pmf(0.0,home.hScored_first,away.aScored_first)
		A = skellam.pmf(-1,home.hScored_first,away.aScored_first)+skellam.pmf(-2,home.hScored_first,away.aScored_first)+skellam.pmf(-3,home.hScored_first,away.aScored_first)+skellam.pmf(-4,home.hScored_first,away.aScored_first)
	elif n ==2:
		H = skellam.pmf(1,home.hScored_second,away.aScored_second)+skellam.pmf(2,home.hScored_second,away.aScored_second)+skellam.pmf(3,home.hScored_second,away.aScored_second)+skellam.pmf(4,home.hScored_second,away.aScored_second)
		D = skellam.pmf(0.0,home.hScored_second,away.aScored_second)
		A = skellam.pmf(-1,home.hScored_second,away.aScored_second)+skellam.pmf(-2,home.hScored_second,away.aScored_second)+skellam.pmf(-3,home.hScored_second,away.aScored_second)+skellam.pmf(-4,home.hScored_second,away.aScored_second)
	else:
		H = skellam.pmf(1,home.hScored_first+home.hScored_second,away.aScored_first+away.aScored_second+away.aScored_second)+skellam.pmf(2,home.hScored_first+home.hScored_second,away.aScored_first+away.aScored_second+away.aScored_second)+skellam.pmf(3,home.hScored_first+home.hScored_second,away.aScored_first+away.aScored_second+away.aScored_second)+skellam.pmf(4,home.hScored_first+home.hScored_second,away.aScored_first+away.aScored_second+away.aScored_second)+skellam.pmf(5,home.hScored_first+home.hScored_second,away.aScored_first+away.aScored_second+away.aScored_second)
		D = skellam.pmf(0.0,home.hScored_first+home.hScored_second,away.aScored_first+away.aScored_second+away.aScored_second)
		A = skellam.pmf(-1,home.hScored_first+home.hScored_second,away.aScored_first+away.aScored_second+away.aScored_second)+skellam.pmf(-2,home.hScored_first+home.hScored_second,away.aScored_first+away.aScored_second+away.aScored_second)+skellam.pmf(-3,home.hScored_first+home.hScored_second,away.aScored_first+away.aScored_second+away.aScored_second)+skellam.pmf(-4,home.hScored_first+home.hScored_second,away.aScored_first+away.aScored_second+away.aScored_second)+skellam.pmf(-5,home.hScored_first+home.hScored_second,away.aScored_first+away.aScored_second+away.aScored_second)
	return H,D,A

def predict_outcome_part_conceded(home, away, n):
	if n==1:
		H = skellam.pmf(1,home.hConceded_first,away.aConceded_first)+skellam.pmf(2,home.hConceded_first,away.aConceded_first)+skellam.pmf(3,home.hConceded_first,away.aConceded_first)+skellam.pmf(4,home.hConceded_first,away.aConceded_first)
		D = skellam.pmf(0.0,home.hConceded_first,away.aConceded_first)
		A = skellam.pmf(-1,home.hConceded_first,away.aConceded_first)+skellam.pmf(-2,home.hConceded_first,away.aConceded_first)+skellam.pmf(-3,home.hConceded_first,away.aConceded_first)+skellam.pmf(-4,home.hConceded_first,away.aConceded_first)
	elif n ==2:
		H = skellam.pmf(1,home.hConceded_second,away.aConceded_second)+skellam.pmf(2,home.hConceded_second,away.aConceded_second)+skellam.pmf(3,home.hConceded_second,away.aConceded_second)+skellam.pmf(4,home.hConceded_second,away.aConceded_second)
		D = skellam.pmf(0.0,home.hConceded_second,away.aConceded_second)
		A = skellam.pmf(-1,home.hConceded_second,away.aConceded_second)+skellam.pmf(-2,home.hConceded_second,away.aConceded_second)+skellam.pmf(-3,home.hConceded_second,away.aConceded_second)+skellam.pmf(-4,home.hConceded_second,away.aConceded_second)
	else:
		H = skellam.pmf(1,home.hConceded_first+home.hConceded_second,away.aConceded_first+away.aConceded_second+away.aConceded_second)+skellam.pmf(2,home.hConceded_first+home.hConceded_second,away.aConceded_first+away.aConceded_second+away.aConceded_second)+skellam.pmf(3,home.hConceded_first+home.hConceded_second,away.aConceded_first+away.aConceded_second+away.aConceded_second)+skellam.pmf(4,home.hConceded_first+home.hConceded_second,away.aConceded_first+away.aConceded_second+away.aConceded_second)+skellam.pmf(5,home.hConceded_first+home.hConceded_second,away.aConceded_first+away.aConceded_second+away.aConceded_second)
		D = skellam.pmf(0.0,home.hConceded_first+home.hConceded_second,away.aConceded_first+away.aConceded_second+away.aConceded_second)
		A = skellam.pmf(-1,home.hConceded_first+home.hConceded_second,away.aConceded_first+away.aConceded_second+away.aConceded_second)+skellam.pmf(-2,home.hConceded_first+home.hConceded_second,away.aConceded_first+away.aConceded_second+away.aConceded_second)+skellam.pmf(-3,home.hConceded_first+home.hConceded_second,away.aConceded_first+away.aConceded_second+away.aConceded_second)+skellam.pmf(-4,home.hConceded_first+home.hConceded_second,away.aConceded_first+away.aConceded_second+away.aConceded_second)+skellam.pmf(-5,home.hConceded_first+home.hConceded_second,away.aConceded_first+away.aConceded_second+away.aConceded_second)
	return H,D,A

def print_result(home,away,arr):
	table = PrettyTable(['',home.name,'Draw', away.name,])
	table.add_row(['Total',int(100*arr[0]),int(100*arr[1]),int(100*arr[2]),])
	table.add_row(['1st Half',int(100*arr[3]),int(100*arr[4]),int(100*arr[5]),])
	table.add_row(['2nd Half',int(100*arr[6]),int(100*arr[7]),int(100*arr[8]),])
	print(table)