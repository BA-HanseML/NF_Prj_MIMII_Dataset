# Application Notes

This document is a collection of consideration / ideas for a solution like developed to be applied in an embedded IoT scenario.

## machine activation, operation modes
If a machine is not permanent active or switches into modes like fan speeds pump speeds etc. it can cause problems ether in interpretation of abnormal or the intent of the supervision. If a machine is not permanent on but only if should be on abnormal is off state this must be incorporated in the use of the supervision. If different operation modes are known and it is possible to comunicate them to the lerning loop this can be incorporated much more robust.

## calibration phase
The current concept works with the all ca. 1000 x 10sec recordings this adds up to above 2.5 hours of training time / recording time. Herby is to notice that maybe a continuous  recording of 2.5 hours at one day in a factory does not create necessary representation of background noise and in cases not necessary enough data for understanding the normal operation of a machine parts. 

On the other hand in some cases it might be sufficient nt to record way lesser. It is extensive challenge to find a good training plan that covers most of the common background events and don't need to long time to become unpractical. Thereby this question is highly dependent on product design specification and can make some solution created here completely unpractical for some use cases.


## what is abnormal in a spectrum or in time - open the black box
Since the decision of abnormal is done based on the spectrum from the perspective of the algorithm it could be helpfull to report back to the user not only the final classification of abnormal or normal but also time frames of abnormal or close to abnormal to increase learning for root cause analytic system. When this is thought further a CNN U-Net and pseudo supervised learning or autoencoder reproduction localized error can be used to create tracing to follow the judgement of the algorithm. 

## Using Clustering and Multi Label
In the beginning of the project we explored unsupervised clustering, even though we opened it as it did not lead to effective way to distinguish normal form abnormal it still can help as analyses tool as it was possible to derive multiple modes of normal that might be not known to the operator and as the training data allows for this type of analyses nearly for free it can be very practically relevant to offer a clustering of recorded times frames. 

This can also be used to steer the training better by operator as it would be possible to exclude extreme background events, that might be excludable ether automatic or manual. Further this can lead to multi class detection if these newly found modes are getting labeled and can create a more granular tracking of the device.


## setting recall or precession modes - sensitivity setting
It might be possible by simple threshold tuning to increase the FN or FP missed abnormality’s over false alarms - with the idea in mind that hard to hear anomaly’s maybe not to bad failures and many false alarms would lead to disabling of the smart sensor in practise, as the mic. can only be extra sensor not safety and not process critical sensor element (at least based on the reached performance for now).

If such modes are established in practise these can be offered as i.e. 3 modes sensitive, neutral and robust where sensitive is most jumpy alarm and conservative alarm while robust is only triggering when the algorithm is very sure something happens.



