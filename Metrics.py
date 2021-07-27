import numpy as np


def mse_loss(y_predict, y):
    return np.mean(np.square(y_predict - y))

def mae_loss(y_predict, y):
    return np.mean(np.abs(y_predict - y))

def flat_y(y_window, window_size):
    y_flat = np.empty((y_window.shape[0], ))
    for i in range(y_window.shape[0]):
        # if i == (y_window.shape[0]-2):
        #     y_flat[i] = (y_window[i, -1, :].reshape(-1) + y_window[i + 1, -2, :].reshape(-1)) / 2
        # if i == (y_window.shape[0]-1):
        #     y_flat[i] = y_window[i, -1, :].reshape(-1)
        try:
            y_flat[i] = (y_window[i, -1,:].reshape(-1) +  y_window[i+1, -2,:].reshape(-1) +
                         y_window[i+2, -3,:].reshape(-1))/3
        except:
            y_flat[i] = y_window[i, -1, :].reshape(-1)
    #y_flat = y_flat[window_size-1:]

    return y_flat

def tp_tn_fp_fn(states_pred, states_ground):
	tp = np.sum(np.logical_and(states_pred == 1, states_ground == 1))
	fp = np.sum(np.logical_and(states_pred == 1, states_ground == 0))
	fn = np.sum(np.logical_and(states_pred == 0, states_ground == 1))
	tn = np.sum(np.logical_and(states_pred == 0, states_ground == 0))
	return tp, tn, fp, fn

def recall_precision_accuracy_f1(pred, ground,threshold):
	pr = np.array([0 if (p)<threshold else 1 for p in pred])
	gr = np.array([0 if p<threshold else 1 for p in ground])

	tp, tn, fp, fn = tp_tn_fp_fn(pr,gr)
	p = np.sum(pr)
	n = len(pr) - p

	res_recall = recall(tp,fn)
	res_precision = precision(tp,fp)
	res_f1 = f1(res_precision,res_recall)
	res_accuracy = accuracy(tp,tn,p,n)

	return (res_recall,res_precision,res_accuracy,res_f1)

def relative_error_total_energy(pred, ground):
	E_pred = np.sum(pred)
	E_ground = np.sum(ground)
	return np.abs(E_pred - E_ground) / float(max(E_pred,E_ground))

def mean_absolute_error(pred, ground):
	total_sum = np.sum(np.abs(pred - ground))

	return total_sum / len(pred)

def recall(tp,fn):
	return tp/float(tp+fn)

def precision(tp,fp):
	return tp/float(tp+fp)

def f1(prec,rec):
	return 2 * (prec*rec) / float(prec+rec)

def accuracy(tp, tn, p, n):
	return (tp + tn) / float(p + n)
