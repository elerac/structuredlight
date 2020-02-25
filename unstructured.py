import numpy as np

def generate(width, height, N, seed=0):
    assert width*height<=2**N, "width*height<=2**N"

    np.random.seed(seed)

    raw = np.random.randint(2, size=(height*width, N))
    index = np.sort(np.unique(raw, return_index=True, axis=0)[1])
    unstructured_pattern = raw[index]
    while True:
        _size = width*height - unstructured_pattern.shape[0]
        if _size<=0:
            break
        raw = np.random.randint(2, size=(_size, N))
        unstructured_pattern = np.concatenate([unstructured_pattern, raw])
        index = np.sort(np.unique(unstructured_pattern, return_index=True, axis=0)[1])
        unstructured_pattern = unstructured_pattern[index]
    
    unstructured_pattern = np.reshape(unstructured_pattern, (height, width, N)).astype(np.uint8)
    unstructured_pattern *= 255
    imgs_unstructured = list(unstructured_pattern.transpose(2, 0, 1))
    return imgs_unstructured

def decode(imgs_cap, imgs_proj):
    import faiss
    height_cap, width_cap = imgs_cap[0].shape[:2]
    height_proj, width_proj = imgs_proj[0].shape[:2]
    assert len(imgs_cap)==len(imgs_proj), "len(imgs_cap)==len(imgs_proj)"
    N = len(imgs_cap)
   
    imgs_cap = imgs_cap - np.average(np.array(imgs_cap), axis=0)
    imgs_proj = imgs_proj - np.average(np.array(imgs_proj), axis=0)
    X = np.ascontiguousarray(np.reshape((np.array(imgs_proj)).transpose((1, 2, 0)), (width_proj*height_proj, N)).astype(np.float32))
    Q = np.ascontiguousarray(np.reshape((np.array(imgs_cap )).transpose((1, 2, 0)), (width_cap *height_cap , N)).astype(np.float32))
    
    #index = faiss.IndexFlatL2(N) #L2 norm
    index = faiss.IndexFlatIP(N) #cos
    index.add(X)

    dists, ids = index.search(x=Q, k=1)
    _ids = np.array([np.unravel_index(i, (height_proj, width_proj)) for i in ids[:,0]])
    index_decode = np.reshape(_ids, (height_cap, width_cap, 2))
    return list(index_decode.transpose(2, 0, 1))


def main():
    import cv2
    import os
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("width", type=int, help="width")
    parser.add_argument("height", type=int, help="height")
    parser.add_argument("N", type=int, help="Number of images")
    parser.add_argument("-o", "--out", type=str, default=".", help="output directory")
    args = parser.parse_args()
    
    width = args.width
    height = args.height
    N = args.N

    #generate unstructured code images
    imgs_unstructured = generate(width, height, N)

    #decode unstructured code images
    #imgs_cap = [cv2.resize(img, None, fx=1.2, fy=1.1) for img in imgs_unstructured]
    #decode_h, decode_v = decode(imgs_cap, imgs_unstructured)

    #export unstructured code images
    out_dir = args.out
    if os.path.isdir(out_dir)==False:
        ret = os.makedirs(out_dir)
        if ret==False:
            print("false mkdir")
            return -1
        else:
            print("mkdir {}".format(out_dir))
   
    print("Export unstructured code images")
    for i, img in enumerate(imgs_unstructured):
        name = os.path.join(out_dir, "unstructured-{0}.png".format(i+1))
        print(name)
        cv2.imwrite(name, img)

if __name__=="__main__":
    main()
