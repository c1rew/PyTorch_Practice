import numpy as np
import torch
N, D_in, H, D_out = 64, 1000, 100, 10 # 64个输入，输入是1000维

# 说明：基于1.2版本，使用torch nn 模型替换手动的模型定义

# 随机创建一些训练数据
x = torch.randn(N, D_in)
y = torch.randn(N, D_out)

model = torch.nn.Sequential(
    torch.nn.Linear(D_in, H),
    torch.nn.ReLU(),
    torch.nn.Linear(H, D_out)
)
# 以下两句，weight初始化为normal，否则模型loss下降特别慢
torch.nn.init.normal_(model[0].weight)
torch.nn.init.normal_(model[2].weight)

loss_fn = torch.nn.MSELoss(reduction='sum')

learning_rate = 1e-6
for it in range(500):
    # Forward pass
    y_pred = model(x)
    
    # compute loss
    loss = loss_fn(y_pred, y)
    print(it, loss.item())
    
    # Backward pass
    # compute the gradient
    model.zero_grad()
    loss.backward()
    with torch.no_grad():
	    # update weights of w1 and w2
        for param in model.parameters():
            param -= learning_rate * param.grad
