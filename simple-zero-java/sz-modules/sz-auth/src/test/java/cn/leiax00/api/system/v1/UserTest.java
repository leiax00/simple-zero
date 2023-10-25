package cn.leiax00.api.system.v1;

import cn.leiax00.common.core.utils.ProtoUtils;
import com.google.protobuf.Any;
import com.google.protobuf.InvalidProtocolBufferException;
import org.junit.jupiter.api.Test;

public class UserTest {
    class TmpUser {
        private String username;
        private String password;

        private TmpUser(String username, String password) {
            this.username = username;
            this.password = password;
        }

        public String getUsername() {
            return username;
        }

        public void setUsername(String username) {
            this.username = username;
        }

        public String getPassword() {
            return password;
        }

        public void setPassword(String password) {
            this.password = password;
        }
    }

    @Test
    public void serializeUserTest() throws InvalidProtocolBufferException {
        TmpUser user = new TmpUser("leiax00", "lax4832.");
        User.UserInfo userInfo = User.UserInfo.newBuilder().setUsername("leiax00").setPassword("lax4832.").build();
        User.UserReply userReply = User.UserReply.newBuilder().setCode(200).setData(Any.pack(userInfo)).build();
        System.out.println(ProtoUtils.proto2JsonStr(userReply, User.UserInfo.getDescriptor()));
    }
}