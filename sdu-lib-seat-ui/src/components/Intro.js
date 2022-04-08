import {Row, Typography} from "antd";

export default function (props)
{
    const { Title, Paragraph, Text, Link } = Typography;

    return (
        <div className={'sdu-lib-seat-intro'}>
            <Typography>
                <Title><Link href={'https://github.com/PTYin/sdu-lib-seat'}>SDU-LIB-SEAT</Link></Title>

                <Paragraph>
                    <Text >SDU-LIB-SEAT</Text>
                    简化山东大学图书馆座位预约流程，经测试现支持济南/青岛/威海各个校区图书馆实现自动预约座位。
                </Paragraph>


                <Title level={2}>使用前须知</Title>

                <Paragraph>
                    <Text strong>
                        项目仅供学习交流使用，这是个不错的<Text code>Python</Text>爬虫学习项目，
                        请不要将其用于商业用途， 更不要有偿出图书馆座位！ <br/>
                        如果项目对您有用，请为<Link href={'https://github.com/PTYin/sdu-lib-seat'}>本项目</Link>点一颗🌟，
                        也欢迎各位同学提issue或pr对本项目进行改进。
                    </Text>
                </Paragraph>


                <Title level={2}>MIT LICENSE</Title>

                <Paragraph style={{display: 'inline-block', textAlign: 'left'}}>
                    <Text italic>Copyright (c) 2022 Xiangkun Yin</Text><br/><br/>

                    Permission is hereby granted, free of charge, to any person obtaining a copy
                    of this software and associated documentation files (the "Software"), to deal
                    in the Software without restriction, including without limitation the rights
                    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
                    copies of the Software, and to permit persons to whom the Software is
                    furnished to do so, subject to the following conditions:<br/><br/>

                    The above copyright notice and this permission notice shall be included in all
                    copies or substantial portions of the Software.<br/><br/>

                    <Text strong>
                        THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
                        IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
                        FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
                        AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
                        LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
                        OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
                        SOFTWARE.
                    </Text>
                </Paragraph>
            </Typography>
        </div>
    )
}