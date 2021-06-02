# from __future__ import absolute_import
# from __future__ import division
# from __future__ import print_function
#
# import cv2
# import numpy as np
#
# import os
# import sys
# from os.path import join, exists
# from os import listdir, makedirs
#
# __dir__ = os.path.dirname(os.path.abspath(__file__))
# sys.path.append(__dir__)
# sys.path.append(os.path.abspath(os.path.join(__dir__, '..')))
#
# os.environ["FLAGS_allocator_strategy"] = 'auto_growth'
#
# import paddle
#
# from ppocr.data import create_operators, transform
# from ppocr.modeling.architectures import build_model
# from ppocr.postprocess import build_post_process
# from ppocr.utils.save_load import init_model
# from ppocr.utils.utility import get_image_file_list
# import tools.program as program
#
#
# def main():
#     global_config = config['Global']
#
#     # build post process
#     post_process_class = build_post_process(config['PostProcess'],
#                                             global_config)
#
#     # build model
#     if hasattr(post_process_class, 'character'):
#         config['Architecture']["Head"]['out_channels'] = len(
#             getattr(post_process_class, 'character'))
#
#     model = build_model(config['Architecture'])
#
#     init_model(config, model, logger)
#
#     # create data ops
#     transforms = []
#     for op in config['Eval']['dataset']['transforms']:
#         op_name = list(op)[0]
#         if 'Label' in op_name:
#             continue
#         elif op_name in ['RecResizeImg']:
#             op[op_name]['infer_mode'] = True
#         elif op_name == 'KeepKeys':
#             if config['Architecture']['algorithm'] == "SRN":
#                 op[op_name]['keep_keys'] = [
#                     'image', 'encoder_word_pos', 'gsrm_word_pos',
#                     'gsrm_slf_attn_bias1', 'gsrm_slf_attn_bias2'
#                 ]
#             else:
#                 op[op_name]['keep_keys'] = ['image']
#         transforms.append(op)
#     global_config['infer_mode'] = True
#     ops = create_operators(transforms, global_config)
#
#     model.eval()
#
#     root = "/home/duytk/RABILOO/OCR/ALL_DATA/org_detect"
#     file = open("test_result2.txt", 'w')
#     img_list = listdir(root)
#     for i, img_name in enumerate(img_list):
#         img_path = join(root, img_name)
#         with open(img_path, 'rb') as f:
#             img = f.read()
#             data = {'image': img}
#         batch = transform(data, ops)
#         if config['Architecture']['algorithm'] == "SRN":
#             encoder_word_pos_list = np.expand_dims(batch[1], axis=0)
#             gsrm_word_pos_list = np.expand_dims(batch[2], axis=0)
#             gsrm_slf_attn_bias1_list = np.expand_dims(batch[3], axis=0)
#             gsrm_slf_attn_bias2_list = np.expand_dims(batch[4], axis=0)
#
#             others = [
#                 paddle.to_tensor(encoder_word_pos_list),
#                 paddle.to_tensor(gsrm_word_pos_list),
#                 paddle.to_tensor(gsrm_slf_attn_bias1_list),
#                 paddle.to_tensor(gsrm_slf_attn_bias2_list)
#             ]
#
#         images = np.expand_dims(batch[0], axis=0)
#         images = paddle.to_tensor(images)
#         b, c, h, w = images.shape
#         images = images[:, :, 2:h - 2, 2:w - 2]
#         if config['Architecture']['algorithm'] == "SRN":
#             preds = model(images, others)
#         else:
#             preds = model(images)
#         post_result = post_process_class(preds)
#         # img_ = cv2.imread(img_path)
#         for rec_reuslt in post_result:
#             logger.info('{}-{}-{}'.format(i, rec_reuslt, img_name))
#             file.write('{}\t{}\t{}\n'.format(img_name, rec_reuslt[0], rec_reuslt[1]))
#
#
# if __name__ == '__main__':
#     config, device, logger, vdl_writer = program.preprocess()
#     main()

import cv2
from os.path import join, exists
from os import listdir, makedirs

root = "/home/duytk/RABILOO/OCR/ALL_DATA/org_detect"
file = open("/home/duytk/RABILOO/OCR/E2E/PaddleOCR/test_result2.txt", 'r')
for line in file.readlines():
    line = line.strip()
    img_name, text, conf = line.split('\t')
    img_path = join(root, img_name)
    image = cv2.imread(img_path)
    h, w, c = image.shape
    image = cv2.resize(image, (int(32 * w / h), 32))
    if image.shape[0] >= 15:
        print(conf, ' : ', text, ' : ', image.shape,h,w, ' : ', img_name)
        cv2.imshow("image", image)
        cv2.waitKey()
